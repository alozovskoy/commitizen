"""
# DESIGN

## Parse CHANGELOG.md

1. Get LATEST VERSION from CONFIG
1. Parse the file version to version
2. Build a dict (tree) of that particular version
3. Transform tree into markdown again

## Parse git log

1. get commits between versions
2. filter commits with the current cz rules
3. parse commit information
4. yield tree nodes
5. format tree nodes
6. produce full tree
7. generate changelog

Extra:
- Generate full or partial changelog
- Include in tree from file all the extra comments added manually
"""
import re
from collections import OrderedDict, defaultdict
from typing import Dict, Generator, Iterable, List, Optional, Type

import pkg_resources
from jinja2 import Template
from typing_extensions import Protocol

from commitizen import defaults
from commitizen.git import GitCommit, GitObject, GitProtocol, GitTag

MD_VERSION_RE = r"^##\s(?P<version>[a-zA-Z0-9.+]+)\s?\(?(?P<date>[0-9-]+)?\)?"
MD_CHANGE_TYPE_RE = r"^###\s(?P<change_type>[a-zA-Z0-9.+\s]+)"
MD_MESSAGE_RE = r"^-\s(\*{2}(?P<scope>[a-zA-Z0-9]+)\*{2}:\s)?(?P<message>.+)(?P<breaking>!)?"
md_version_c = re.compile(MD_VERSION_RE)
md_change_type_c = re.compile(MD_CHANGE_TYPE_RE)
md_message_c = re.compile(MD_MESSAGE_RE)


CATEGORIES = [
    ("fix", "fix"),
    ("breaking", "BREAKING CHANGES"),
    ("feat", "feat"),
    ("refactor", "refactor"),
    ("perf", "perf"),
    ("test", "test"),
    ("build", "build"),
    ("ci", "ci"),
    ("chore", "chore"),
]


def find_version_blocks(filepath: str) -> Generator:
    """
    version block: contains all the information about a version.

    E.g:
    ```
    ## 1.2.1 (2019-07-20)

    ### Fix

    - username validation not working

    ### Feat

    - new login system

    ```
    """
    with open(filepath, "r") as f:
        block: list = []
        for line in f:
            line = line.strip("\n")
            if not line:
                continue

            if line.startswith("## "):
                if len(block) > 0:
                    yield block
                block = [line]
            else:
                block.append(line)
        yield block


def parse_md_version(md_version: str) -> Dict:
    m = md_version_c.match(md_version)
    if not m:
        return {}
    return m.groupdict()


def parse_md_change_type(md_change_type: str) -> Dict:
    m = md_change_type_c.match(md_change_type)
    if not m:
        return {}
    return m.groupdict()


def parse_md_message(md_message: str) -> Dict:
    m = md_message_c.match(md_message)
    if not m:
        return {}
    return m.groupdict()


def transform_change_type(change_type: str) -> str:
    # TODO: Use again to parse, for this we have to wait until the maps get
    # defined again.
    _change_type_lower = change_type.lower()
    for match_value, output in CATEGORIES:
        if re.search(match_value, _change_type_lower):
            return output
    else:
        raise ValueError(f"Could not match a change_type with {change_type}")


def generate_block_tree(block: List[str]) -> Dict:
    # tree: Dict = {"commits": []}
    changes: Dict = defaultdict(list)
    tree: Dict = {"changes": changes}

    change_type = None
    for line in block:
        if line.startswith("## "):
            # version identified
            change_type = None
            tree = {**tree, **parse_md_version(line)}
        elif line.startswith("### "):
            # change_type identified
            result = parse_md_change_type(line)
            if not result:
                continue
            change_type = result.get("change_type", "").lower()

        elif line.startswith("- "):
            # message identified
            commit = parse_md_message(line)
            changes[change_type].append(commit)
        else:
            print("it's something else: ", line)
    return tree


def generate_full_tree(blocks: Iterable) -> Iterable[Dict]:
    for block in blocks:
        yield generate_block_tree(block)


def get_commit_tag(commit: GitProtocol, tags: List[GitProtocol]) -> Optional[GitTag]:
    """"""
    try:
        tag_index = tags.index(commit)
    except ValueError:
        return None
    else:
        tag = tags[tag_index]
        # if hasattr(tag, "name"):
        return tag


def generate_tree_from_commits(
    commits: List[GitCommit],
    tags: List[GitTag],
    commit_parser: str,
    changelog_pattern: str = defaults.bump_pattern,
) -> Iterable[Dict]:
    pat = re.compile(changelog_pattern)
    map_pat = re.compile(commit_parser)
    # Check if the latest commit is not tagged
    latest_commit = commits[0]
    current_tag: Optional[GitTag] = get_commit_tag(latest_commit, tags)

    current_tag_name: str = "Unreleased"
    current_tag_date: str = ""
    if current_tag is not None and current_tag.name:
        current_tag_name = current_tag.name
        current_tag_date = current_tag.date

    changes: Dict = defaultdict(list)
    used_tags: List = [current_tag]
    for commit in commits:
        commit_tag = get_commit_tag(commit, tags)

        if commit_tag is not None and commit_tag not in used_tags:
            used_tags.append(commit_tag)
            yield {
                "version": current_tag_name,
                "date": current_tag_date,
                "changes": changes,
            }
            # TODO: Check if tag matches the version pattern, otherwie skip it.
            # This in order to prevent tags that are not versions.
            current_tag_name = commit_tag.name
            current_tag_date = commit_tag.date
            changes = defaultdict(list)

        matches = pat.match(commit.message)
        if not matches:
            continue

        message = map_pat.match(commit.message)
        message_body = map_pat.match(commit.body)
        if message:
            parsed_message: Dict = message.groupdict()
            change_type = parsed_message.pop("change_type")
            changes[change_type].append(parsed_message)
        if message_body:
            parsed_message_body: Dict = message_body.groupdict()
            change_type = parsed_message_body.pop("change_type")
            changes[change_type].append(parsed_message_body)

    yield {
        "version": current_tag_name,
        "date": current_tag_date,
        "changes": changes,
    }


def render_changelog(tree: Iterable) -> str:
    template_file = pkg_resources.resource_string(
        __name__, "templates/keep_a_changelog_template.j2"
    ).decode("utf-8")
    jinja_template = Template(template_file, trim_blocks=True)
    changelog: str = jinja_template.render(tree=tree)
    return changelog
