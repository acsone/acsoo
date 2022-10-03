# -*- coding: utf-8 -*-
# Copyright 2016-2020 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import re
import tempfile

import click

from .main import main
from .tools import call, check_call, check_output

_logger = logging.getLogger(__name__)


RE = re.compile(
    r"(?P<editable>(-e|--editable) +)?"
    r"((?P<name>[a-zA-Z0-9-_\.]+)[\[\]a-zA-Z0-9-_\.]* *@ *)?"
    r"(?P<vcs>(git|svn|hg))\+"
    r"(?P<url>(ssh|http|https)://.*?/.*?)@(?P<sha>[^?#&]+)"
    r"(.*?[#?&]egg=(?P<egg>[^?#&]+))?"
)
NOTAG_RE = re.compile(
    r"([a-zA-Z0-9-_\.]+==)|" r"(-f )|(--find-links )|" r"(--extra-index-url )"
)
GIT_URL_RE = re.compile(
    r"(?P<scheme>ssh|http|https)://"
    r"(?P<user>git@)?(?P<host>.*?)/"
    r"(?P<org>.*?)/(?P<rest>.*)"
)


def _make_push_url(config, url):
    mo = GIT_URL_RE.match(url)
    if not mo:
        return False
    groups = mo.groupdict()
    if groups["scheme"] == "ssh":
        return url
    pushkey = groups["host"].lower() + ":" + groups["org"].lower()
    if pushkey not in config.pushable:
        return False
    return "ssh://git@{host}/{org}/{rest}".format(**groups)


def _get_last_sha(filename):
    # find the short sha of the last commit to filename
    return check_output(["git", "log", "-n", "1", "--format=%h", filename]).strip()


def _has_tag_local(series, sha, repo_dir):
    tag_re = re.compile(series + "[-_]")
    tags = check_output(["git", "tag", "--points-at", sha], cwd=repo_dir)
    for tag in tags.split():
        tag = tag.strip()
        if tag_re.match(tag):
            return tag
    return False


def _has_tag_remote(series, sha, repo_url):
    prefix = "refs/tags/"
    tag_re = re.compile(prefix + series + "[-_]")
    tag_lines = check_output(
        ["git", "ls-remote", "-t", repo_url], universal_newlines=True
    )
    for tag_line in tag_lines.split("\n"):
        if not tag_line:
            continue
        remote_sha, ref = tag_line.split()
        if remote_sha == sha and tag_re.match(ref):
            return ref[len(prefix) :]
    return False


def _is_committed(requirement):
    out = check_output(["git", "ls-files", requirement])
    if not out:
        return False
    r = call(["git", "diff", "--exit-code", requirement])
    return r == 0


def _ensure_tag(config, req, sha, repo_url, eggtag, dry_run):
    ex_tag = _has_tag_remote(config.series, sha, repo_url)
    if ex_tag:
        click.echo("tag {ex_tag} already exists on {repo_url}@{sha}".format(**locals()))
        return
    push_url = _make_push_url(config, repo_url)
    if not push_url:
        _logger.warning("Cannot tag %s (not pushable)", req)
        return
    with tempfile.TemporaryDirectory() as repo_dir:
        check_call(["git", "clone", "--bare", push_url, repo_dir])
        click.echo("placing tag {eggtag} on {push_url}@{sha}".format(**locals()))
        if not dry_run:
            check_call(["git", "tag"] + [eggtag, sha], cwd=repo_dir)
            check_call(["git", "push"] + [push_url, eggtag], cwd=repo_dir)


def do_tag_requirements(config, src, requirement, yes, dry_run=False):
    if not _is_committed(requirement):
        raise click.ClickException("Please commit {} first.".format(requirement))
    requirement_sha = _get_last_sha(requirement)
    base_tag = "{}-{}-{}".format(config.series, config.trigram, requirement_sha)
    if not yes:
        click.confirm("Tag dependencies with {}?".format(base_tag), abort=True)
    for req in open(requirement):
        req = req.strip()
        mo = RE.match(req)
        if not mo:
            if not NOTAG_RE.match(req):
                _logger.warning("Cannot not tag %s (unrecognized req)", req)
            continue
        editable = bool(mo.group("editable"))
        vcs = mo.group("vcs")
        url = mo.group("url")
        egg = mo.group("egg") or mo.group("name")
        sha = mo.group("sha")
        eggtag = base_tag + "-" + egg
        if vcs != "git":
            _logger.warning("Cannot tag %s (unsupported vcs)", req)
            continue
        if not editable:
            _ensure_tag(config, req, sha, url, eggtag, dry_run)
            continue
        repo_dir = os.path.join(src, egg.replace("_", "-"))
        if not os.path.isdir(os.path.join(repo_dir, ".git")):
            os.makedirs(repo_dir)
            check_call(["git", "init"], cwd=repo_dir)
        ex_tag = _has_tag_local(config.series, sha, repo_dir)
        if ex_tag:
            # this assumes that if we find the tag locally
            # it is also present on the remote, in rare situations
            # this may not be the case, but this is so much more
            # performant that it's probably worth taking this shortcut.
            click.echo("tag {ex_tag} already exists on {url}@{sha}".format(**locals()))
            continue
        check_call(
            [
                "git",
                "fetch",
                "-q",
                "-f",
                "--tags",
                url,
                "+refs/heads/*:refs/remotes/acsoo/*",
            ],
            cwd=repo_dir,
        )
        ex_tag = _has_tag_local(config.series, sha, repo_dir)
        if ex_tag:
            click.echo("tag {ex_tag} already exists on {url}@{sha}".format(**locals()))
            continue
        push_url = _make_push_url(config, url)
        if not push_url:
            _logger.warning("Cannot tag %s (not pushable)", req)
            continue
        click.echo("placing tag {eggtag} on {push_url}@{sha}".format(**locals()))
        if not dry_run:
            check_call(["git", "tag"] + [eggtag, sha], cwd=repo_dir)
            try:
                check_call(["git", "push"] + [push_url, eggtag], cwd=repo_dir)
            except:  # noqa
                # if push failed, delete local tag
                call(["git", "tag", "-d", eggtag], cwd=repo_dir)
                raise


@click.command()
@click.option(
    "--src",
    default="src",
    envvar="PIP_SRC",
    type=click.Path(file_okay=False),
    help="Directory where editable requirements are checked out",
)
@click.option(
    "-r",
    "--requirement",
    default="requirements.txt",
    type=click.Path(dir_okay=False, exists=True),
    help="Requirements file to use (default=requirements.txt)",
)
@click.option("-y", "--yes", is_flag=True, default=False)
@click.option("--dry-run", is_flag=True, default=False)
@click.pass_context
def tag_requirements(ctx, src, requirement, yes, dry_run):
    """Tag all VCS requirements found in requirements.txt.

    This is important to avoid that commits referenced in requirements.txt
    are lost in case of VCS garbage collection.

    Only git is supported for now.

    Tags created have the form {series}-{trigram}-{sha1}, where series and
    trigram come from acsoo.cfg, and sha1 is the short sha of the project
    at the time when we create the tag. At the end of the day, this tag
    structure does not really matter, as it is only meant to avoid git
    garbage collection of commits referenced in requirements.txt,
    and not to be retrieved manually.

    Tags created are pushed to the corresponding repository.
    The list of repositories/organizations where we can push can be configured
    in acsoo.cfg like this (the default is github.com:acsone):

    \b
    [acsoo]
    trigram=xyz
    series=10.0
    pushable =
      github.com:acsone
      github.com:mozaik
    """
    do_tag_requirements(ctx.obj["config"], src, requirement, yes, dry_run)


main.add_command(tag_requirements)
