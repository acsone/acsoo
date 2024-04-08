# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import re
from collections import namedtuple

import click
import httpx

from .main import main

_logger = logging.getLogger(__name__)


PR = namedtuple("PR", ["org", "repo", "pr"])
PR_RE = re.compile(
    r".*github.com.(?P<org>[^/]+)/(?P<repo>[^/]+)" r".*@refs/pull/(?P<pr>[0-9]+)/head"
)
PR_URL_RE = re.compile(
    r".*https://github.com/(?P<org>[^/]+)/(?P<repo>[^/]+)/pull/(?P<pr>[0-9]+).*"
)


def looks_like_req_file(filename):
    return ("requirements" in filename or "constraints" in filename) and (
        filename.endswith(".txt") or filename.endswith(".txt.in")
    )


def display_state(rjson):
    state = rjson["state"]
    merged = rjson["merged"]
    if state == "open":
        return click.style("open", fg="white")
    elif state == "closed" and merged:
        return click.style("merged", fg="magenta")
    elif state == "closed" and not merged:
        return click.style("closed", fg="red")
    else:
        return click.style(state, fg="yellow")


def search_prs():
    for reqfile in os.listdir("."):
        if not looks_like_req_file(reqfile):
            continue
        click.secho("Scanning " + reqfile, dim=True)
        with open(reqfile) as f:
            for line in f:
                mo = PR_RE.match(line) or PR_URL_RE.match(line)
                if not mo:
                    continue
                yield PR(**mo.groupdict())


@click.command()
def pr_status():
    """Show status of PR found in requirement files.

    If set, the GITHUB_TOKEN environment variable is used to authenticate with the
    GitHub API and avoid rate limiting.
    """
    # get github token from env
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        httpx_client = httpx.Client(headers={"Authorization": f"token {token}"})
    else:
        click.echo("No GITHUB_TOKEN found in env, using anonymous access")
        httpx_client = httpx.Client()
    for pr in search_prs():
        r = httpx_client.get(
            f"https://api.github.com/repos/{pr.org}/{pr.repo}/pulls/{pr.pr}"
        )
        r.raise_for_status()
        state = display_state(r.json())
        click.echo(f"https://github.com/{pr.org}/{pr.repo}/pull/{pr.pr} is {state}")


main.add_command(pr_status)
