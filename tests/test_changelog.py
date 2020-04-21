import os

import pytest
from commitizen import changelog, git, defaults


COMMIT_LOG = [
    "bump: version 1.5.0 → 1.5.1",
    "",
    "Merge pull request #29 from esciara/issue_28",
    "fix: #28 allows poetry add on py36 envs",
    "fix: #28 allows poetry add on py36 envs",
    "",
    "Merge pull request #26 from Woile/dependabot/pip/black-tw-19.3b0",
    "chore(deps-dev): update black requirement from ^18.3-alpha.0 to ^19.3b0",
    "Merge pull request #27 from Woile/dependabot/pip/mypy-tw-0.701",
    "chore(deps-dev): update mypy requirement from ^0.700.0 to ^0.701",
    "chore(deps-dev): update mypy requirement from ^0.700.0 to ^0.701",
    (
        "Updates the requirements on "
        "[mypy](https://github.com/python/mypy) to permit the latest version."
    ),
    "- [Release notes](https://github.com/python/mypy/releases)",
    "- [Commits](https://github.com/python/mypy/compare/v0.700...v0.701)",
    "",
    "Signed-off-by: dependabot[bot] <support@dependabot.com>",
    "chore(deps-dev): update black requirement from ^18.3-alpha.0 to ^19.3b0",
    (
        "Updates the requirements on [black](https://github.com/ambv/black)"
        " to permit the latest version."
    ),
    "- [Release notes](https://github.com/ambv/black/releases)",
    "- [Commits](https://github.com/ambv/black/commits)",
    "",
    "Signed-off-by: dependabot[bot] <support@dependabot.com>",
    "bump: version 1.4.0 → 1.5.0",
    "",
    "docs: add info about extra pattern in the files when bumping",
    "",
    (
        "feat(bump): it is now possible to specify a pattern "
        "in the files attr to replace the version"
    ),
    "",
]

CHANGELOG_TEMPLATE = """
## 1.0.0 (2019-07-12)

### Fix

- issue in poetry add preventing the installation in py36
- **users**: lorem ipsum apap

### Feat

- it is possible to specify a pattern to be matched in configuration files bump.

## 0.9 (2019-07-11)

### Fix

- holis

"""


COMMITS_DATA = [
    {
        "rev": "141ee441c9c9da0809c554103a558eb17c30ed17",
        "title": "bump: version 1.1.1 → 1.2.0",
        "body": "",
    },
    {
        "rev": "6c4948501031b7d6405b54b21d3d635827f9421b",
        "title": "docs: how to create custom bumps",
        "body": "",
    },
    {
        "rev": "ddd220ad515502200fe2dde443614c1075d26238",
        "title": "feat: custom cz plugins now support bumping version",
        "body": "",
    },
    {
        "rev": "ad17acff2e3a2e141cbc3c6efd7705e4e6de9bfc",
        "title": "docs: added bump gif",
        "body": "",
    },
    {
        "rev": "56c8a8da84e42b526bcbe130bd194306f7c7e813",
        "title": "bump: version 1.1.0 → 1.1.1",
        "body": "",
    },
    {
        "rev": "74c6134b1b2e6bb8b07ed53410faabe99b204f36",
        "title": "refactor: changed stdout statements",
        "body": "",
    },
    {
        "rev": "cbc7b5f22c4e74deff4bc92d14e19bd93524711e",
        "title": "fix(bump): commit message now fits better with semver",
        "body": "",
    },
    {
        "rev": "1ba46f2a63cb9d6e7472eaece21528c8cd28b118",
        "title": "fix: conventional commit 'breaking change' in body instead of title",
        "body": "closes #16",
    },
    {
        "rev": "c35dbffd1bb98bb0b3d1593797e79d1c3366af8f",
        "title": "refactor(schema): command logic removed from commitizen base",
        "body": "",
    },
    {
        "rev": "25313397a4ac3dc5b5c986017bee2a614399509d",
        "title": "refactor(info): command logic removed from commitizen base",
        "body": "",
    },
    {
        "rev": "d2f13ac41b4e48995b3b619d931c82451886e6ff",
        "title": "refactor(example): command logic removed from commitizen base",
        "body": "",
    },
    {
        "rev": "d839e317e5b26671b010584ad8cc6bf362400fa1",
        "title": "refactor(commit): moved most of the commit logic to the commit command",
        "body": "",
    },
    {
        "rev": "12d0e65beda969f7983c444ceedc2a01584f4e08",
        "title": "docs(README): updated documentation url)",
        "body": "",
    },
    {
        "rev": "fb4c85abe51c228e50773e424cbd885a8b6c610d",
        "title": "docs: mkdocs documentation",
        "body": "",
    },
    {
        "rev": "17efb44d2cd16f6621413691a543e467c7d2dda6",
        "title": "Bump version 1.0.0 → 1.1.0",
        "body": "",
    },
    {
        "rev": "6012d9eecfce8163d75c8fff179788e9ad5347da",
        "title": "test: fixed issues with conf",
        "body": "",
    },
    {
        "rev": "0c7fb0ca0168864dfc55d83c210da57771a18319",
        "title": "docs(README): some new information about bump",
        "body": "",
    },
    {
        "rev": "cb1dd2019d522644da5bdc2594dd6dee17122d7f",
        "title": "feat: new working bump command",
        "body": "",
    },
    {
        "rev": "9c7450f85df6bf6be508e79abf00855a30c3c73c",
        "title": "feat: create version tag",
        "body": "",
    },
    {
        "rev": "9f3af3772baab167e3fd8775d37f041440184251",
        "title": "docs: added new changelog",
        "body": "",
    },
    {
        "rev": "b0d6a3defbfde14e676e7eb34946409297d0221b",
        "title": "feat: update given files with new version",
        "body": "",
    },
    {
        "rev": "d630d07d912e420f0880551f3ac94e933f9d3beb",
        "title": "fix: removed all from commit",
        "body": "",
    },
    {
        "rev": "1792b8980c58787906dbe6836f93f31971b1ec2d",
        "title": "feat(config): new set key, used to set version to cfg",
        "body": "",
    },
    {
        "rev": "52def1ea3555185ba4b936b463311949907e31ec",
        "title": "feat: support for pyproject.toml",
        "body": "",
    },
    {
        "rev": "3127e05077288a5e2b62893345590bf1096141b7",
        "title": "feat: first semantic version bump implementaiton",
        "body": "",
    },
    {
        "rev": "fd480ed90a80a6ffa540549408403d5b60d0e90c",
        "title": "fix: fix config file not working",
        "body": "",
    },
    {
        "rev": "e4840a059731c0bf488381ffc77e989e85dd81ad",
        "title": "refactor: added commands folder, better integration with decli",
        "body": "",
    },
    {
        "rev": "aa44a92d68014d0da98965c0c2cb8c07957d4362",
        "title": "Bump version: 1.0.0b2 → 1.0.0",
        "body": "",
    },
    {
        "rev": "58bb709765380dbd46b74ce6e8978515764eb955",
        "title": "docs(README): new badges",
        "body": "",
    },
    {
        "rev": "97afb0bb48e72b6feca793091a8a23c706693257",
        "title": "Merge pull request #10 from Woile/feat/decli",
        "body": "Feat/decli",
    },
    {
        "rev": "9cecb9224aa7fa68d4afeac37eba2a25770ef251",
        "title": "style: black to files",
        "body": "",
    },
    {
        "rev": "f5781d1a2954d71c14ade2a6a1a95b91310b2577",
        "title": "ci: added travis",
        "body": "",
    },
    {
        "rev": "80105fb3c6d45369bc0cbf787bd329fba603864c",
        "title": "refactor: removed delegator, added decli and many tests",
        "body": "BREAKING CHANGE: API is stable",
    },
    {
        "rev": "a96008496ffefb6b1dd9b251cb479eac6a0487f7",
        "title": "docs: updated test command",
        "body": "",
    },
    {
        "rev": "aab33d13110f26604fb786878856ec0b9e5fc32b",
        "title": "Bump version: 1.0.0b1 → 1.0.0b2",
        "body": "",
    },
    {
        "rev": "b73791563d2f218806786090fb49ef70faa51a3a",
        "title": "docs(README): updated to reflect current state",
        "body": "",
    },
    {
        "rev": "7aa06a454fb717408b3657faa590731fb4ab3719",
        "title": "Merge pull request #9 from Woile/dev",
        "body": "feat: py3 only, tests and conventional commits 1.0",
    },
    {
        "rev": "7c7e96b723c2aaa1aec3a52561f680adf0b60e97",
        "title": "Bump version: 0.9.11 → 1.0.0b1",
        "body": "",
    },
    {
        "rev": "ed830019581c83ba633bfd734720e6758eca6061",
        "title": "feat: py3 only, tests and conventional commits 1.0",
        "body": "more tests\npyproject instead of Pipfile\nquestionary instead of whaaaaat (promptkit 2.0.0 support)",
    },
    {
        "rev": "c52eca6f74f844ab3ffbde61d98ef96071e132b7",
        "title": "Bump version: 0.9.10 → 0.9.11",
        "body": "",
    },
    {
        "rev": "0326652b2657083929507ee66d4d1a0899e861ba",
        "title": "fix(config): load config reads in order without failing if there is no commitizen section",
        "body": "Closes #8",
    },
    {
        "rev": "b3f89892222340150e32631ae6b7aab65230036f",
        "title": "Bump version: 0.9.9 → 0.9.10",
        "body": "",
    },
    {
        "rev": "5e837bf8ef0735193597372cd2d85e31a8f715b9",
        "title": "fix: parse scope (this is my punishment for not having tests)",
        "body": "",
    },
    {
        "rev": "684e0259cc95c7c5e94854608cd3dcebbd53219e",
        "title": "Bump version: 0.9.8 → 0.9.9",
        "body": "",
    },
    {
        "rev": "ca38eac6ff09870851b5c76a6ff0a2a8e5ecda15",
        "title": "fix: parse scope empty",
        "body": "",
    },
    {
        "rev": "64168f18d4628718c49689ee16430549e96c5d4b",
        "title": "Bump version: 0.9.7 → 0.9.8",
        "body": "",
    },
    {
        "rev": "9d4def716ef235a1fa5ae61614366423fbc8256f",
        "title": "fix(scope): parse correctly again",
        "body": "",
    },
    {
        "rev": "33b0bf1a0a4dc60aac45ed47476d2e5473add09e",
        "title": "Bump version: 0.9.6 → 0.9.7",
        "body": "",
    },
    {
        "rev": "696885e891ec35775daeb5fec3ba2ab92c2629e1",
        "title": "fix(scope): parse correctly",
        "body": "",
    },
    {
        "rev": "bef4a86761a3bda309c962bae5d22ce9b57119e4",
        "title": "Bump version: 0.9.5 → 0.9.6",
        "body": "",
    },
    {
        "rev": "72472efb80f08ee3fd844660afa012c8cb256e4b",
        "title": "refactor(conventionalCommit): moved fitlers to questions instead of message",
        "body": "",
    },
    {
        "rev": "b5561ce0ab3b56bb87712c8f90bcf37cf2474f1b",
        "title": "fix(manifest): inluded missing files",
        "body": "",
    },
    {
        "rev": "3e31714dc737029d96898f412e4ecd2be1bcd0ce",
        "title": "Bump version: 0.9.4 → 0.9.5",
        "body": "",
    },
    {
        "rev": "9df721e06595fdd216884c36a28770438b4f4a39",
        "title": "fix(config): home path for python versions between 3.0 and 3.5",
        "body": "",
    },
    {
        "rev": "0cf6ada372470c8d09e6c9e68ebf94bbd5a1656f",
        "title": "Bump version: 0.9.3 → 0.9.4",
        "body": "",
    },
    {
        "rev": "973c6b3e100f6f69a3fe48bd8ee55c135b96c318",
        "title": "feat(cli): added version",
        "body": "",
    },
    {
        "rev": "dacc86159b260ee98eb5f57941c99ba731a01399",
        "title": "Bump version: 0.9.2 → 0.9.3",
        "body": "",
    },
    {
        "rev": "4368f3c3cbfd4a1ced339212230d854bc5bab496",
        "title": "feat(commiter): conventional commit is a bit more intelligent now",
        "body": "",
    },
    {
        "rev": "da94133288727d35dae9b91866a25045038f2d38",
        "title": "docs(README): motivation",
        "body": "",
    },
    {
        "rev": "1541f54503d2e1cf39bd777c0ca5ab5eb78772ba",
        "title": "Bump version: 0.9.1 → 0.9.2",
        "body": "",
    },
    {
        "rev": "ddc855a637b7879108308b8dbd85a0fd27c7e0e7",
        "title": "refactor: renamed conventional_changelog to conventional_commits, not backward compatible",
        "body": "",
    },
    {
        "rev": "46e9032e18a819e466618c7a014bcb0e9981af9e",
        "title": "Bump version: 0.9.0 → 0.9.1",
        "body": "",
    },
    {
        "rev": "0fef73cd7dc77a25b82e197e7c1d3144a58c1350",
        "title": "fix(setup.py): future is now required for every python version",
        "body": "",
    },
]


TAGS = [
    ("v1.2.0", "141ee441c9c9da0809c554103a558eb17c30ed17", "2019-04-19"),
    ("v1.1.1", "56c8a8da84e42b526bcbe130bd194306f7c7e813", "2019-04-18"),
    ("v1.1.0", "17efb44d2cd16f6621413691a543e467c7d2dda6", "2019-04-14"),
    ("v1.0.0", "aa44a92d68014d0da98965c0c2cb8c07957d4362", "2019-03-01"),
    ("1.0.0b2", "aab33d13110f26604fb786878856ec0b9e5fc32b", "2019-01-18"),
    ("v1.0.0b1", "7c7e96b723c2aaa1aec3a52561f680adf0b60e97", "2019-01-17"),
    ("v0.9.11", "c52eca6f74f844ab3ffbde61d98ef96071e132b7", "2018-12-17"),
    ("v0.9.10", "b3f89892222340150e32631ae6b7aab65230036f", "2018-09-22"),
    ("v0.9.9", "684e0259cc95c7c5e94854608cd3dcebbd53219e", "2018-09-22"),
    ("v0.9.8", "64168f18d4628718c49689ee16430549e96c5d4b", "2018-09-22"),
    ("v0.9.7", "33b0bf1a0a4dc60aac45ed47476d2e5473add09e", "2018-09-22"),
    ("v0.9.6", "bef4a86761a3bda309c962bae5d22ce9b57119e4", "2018-09-19"),
    ("v0.9.5", "3e31714dc737029d96898f412e4ecd2be1bcd0ce", "2018-08-24"),
    ("v0.9.4", "0cf6ada372470c8d09e6c9e68ebf94bbd5a1656f", "2018-08-02"),
    ("v0.9.3", "dacc86159b260ee98eb5f57941c99ba731a01399", "2018-07-28"),
    ("v0.9.2", "1541f54503d2e1cf39bd777c0ca5ab5eb78772ba", "2017-11-11"),
    ("v0.9.1", "46e9032e18a819e466618c7a014bcb0e9981af9e", "2017-11-11"),
]


@pytest.fixture
def gitcommits() -> list:
    commits = [
        git.GitCommit(commit["rev"], commit["title"], commit["body"])
        for commit in COMMITS_DATA
    ]
    return commits


@pytest.fixture
def tags() -> list:
    tags = [git.GitTag(*tag) for tag in TAGS]
    return tags


@pytest.fixture
def changelog_content() -> str:
    changelog_path = "tests/CHANGELOG_FOR_TEST.md"
    with open(changelog_path, "r") as f:
        return f.read()


@pytest.fixture
def existing_changelog_file(request):
    changelog_path = "tests/CHANGELOG.md"

    with open(changelog_path, "w") as f:
        f.write(CHANGELOG_TEMPLATE)

    yield changelog_path

    os.remove(changelog_path)


def test_read_changelog_blocks(existing_changelog_file):
    blocks = changelog.find_version_blocks(existing_changelog_file)
    blocks = list(blocks)
    amount_of_blocks = len(blocks)
    assert amount_of_blocks == 2


VERSION_CASES: list = [
    ("## 1.0.0 (2019-07-12)", {"version": "1.0.0", "date": "2019-07-12"}),
    ("## 2.3.0a0", {"version": "2.3.0a0", "date": None}),
    ("## 0.10.0a0", {"version": "0.10.0a0", "date": None}),
    ("## 1.0.0rc0", {"version": "1.0.0rc0", "date": None}),
    ("## 1beta", {"version": "1beta", "date": None}),
    (
        "## 1.0.0rc1+e20d7b57f3eb (2019-3-24)",
        {"version": "1.0.0rc1+e20d7b57f3eb", "date": "2019-3-24"},
    ),
    ("### Bug fixes", {}),
    ("- issue in poetry add preventing the installation in py36", {}),
]

CATEGORIES_CASES: list = [
    ("## 1.0.0 (2019-07-12)", {}),
    ("## 2.3.0a0", {}),
    ("### Bug fixes", {"change_type": "Bug fixes"}),
    ("### Features", {"change_type": "Features"}),
    ("- issue in poetry add preventing the installation in py36", {}),
]

CATEGORIES_TRANSFORMATIONS: list = [
    ("Bug fixes", "fix"),
    ("Features", "feat"),
    ("BREAKING CHANGES", "BREAKING CHANGES"),
]

MESSAGES_CASES: list = [
    ("## 1.0.0 (2019-07-12)", {}),
    ("## 2.3.0a0", {}),
    ("### Fix", {}),
    (
        "- name no longer accept invalid chars",
        {"message": "name no longer accept invalid chars", "scope": None, "breaking": None},
    ),
    (
        "- **users**: lorem ipsum apap",
        {"message": "lorem ipsum apap", "scope": "users", "breaking": None},
    ),
]


@pytest.mark.parametrize("test_input,expected", VERSION_CASES)
def test_parse_md_version(test_input, expected):
    assert changelog.parse_md_version(test_input) == expected


@pytest.mark.parametrize("test_input,expected", CATEGORIES_CASES)
def test_parse_md_change_type(test_input, expected):
    assert changelog.parse_md_change_type(test_input) == expected


@pytest.mark.parametrize("test_input,expected", CATEGORIES_TRANSFORMATIONS)
def test_transform_change_type(test_input, expected):
    assert changelog.transform_change_type(test_input) == expected


@pytest.mark.parametrize("test_input,expected", MESSAGES_CASES)
def test_parse_md_message(test_input, expected):
    assert changelog.parse_md_message(test_input) == expected


def test_transform_change_type_fail():
    with pytest.raises(ValueError) as excinfo:
        changelog.transform_change_type("Bugs")
    assert "Could not match a change_type" in str(excinfo.value)


def test_generate_block_tree(existing_changelog_file):
    blocks = changelog.find_version_blocks(existing_changelog_file)
    block = next(blocks)
    tree = changelog.generate_block_tree(block)
    assert tree == {
        "changes": {
            "fix": [
                {
                    "scope": None,
                    "breaking": None,
                    "message": "issue in poetry add preventing the installation in py36",
                },
                {"scope": "users", "breaking": None, "message": "lorem ipsum apap"},
            ],
            "feat": [
                {
                    "scope": None,
                    "breaking": None,
                    "message": (
                        "it is possible to specify a pattern to be matched "
                        "in configuration files bump."
                    ),
                }
            ],
        },
        "version": "1.0.0",
        "date": "2019-07-12",
    }


def test_generate_full_tree(existing_changelog_file):
    blocks = changelog.find_version_blocks(existing_changelog_file)
    tree = list(changelog.generate_full_tree(blocks))

    assert tree == [
        {
            'changes': {
                'fix': [
                    {
                        'scope': None,
                        'message': 'issue in poetry add preventing the installation in py36',
                        'breaking': None,
                    },
                    {
                        'scope': 'users',
                        'message': 'lorem ipsum apap',
                        'breaking': None,
                    },
                ],
                'feat': [
                    {
                        'scope': None,
                        'message': 'it is possible to specify a pattern to be matched in configuration files bump.',
                        'breaking': None,
                    },
                ],
            },
            'version': '1.0.0',
            'date': '2019-07-12',
        },
        {
            'changes': {
                'fix': [
                    {
                        'scope': None,
                        'message': 'holis',
                        'breaking': None,
                    },
                ],
            },
            'version': '0.9',
            'date': '2019-07-11',
        },
    ]


def test_get_commit_tag_is_a_version(gitcommits, tags):
    commit = gitcommits[0]
    tag = git.GitTag(*TAGS[0])
    current_key = changelog.get_commit_tag(commit, tags)
    assert current_key == tag


def test_get_commit_tag_is_None(gitcommits, tags):
    commit = gitcommits[1]
    current_key = changelog.get_commit_tag(commit, tags)
    assert current_key is None


def test_generate_tree_from_commits(gitcommits, tags):
    parser = defaults.commit_parser
    changelog_pattern = defaults.bump_pattern
    tree = changelog.generate_tree_from_commits(
        gitcommits, tags, parser, changelog_pattern
    )

    assert tuple(tree) == (
        {
            "version": "v1.2.0",
            "date": "2019-04-19",
            "changes": {
                "feat": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "custom cz plugins now support bumping version",
                    }
                ]
            },
        },
        {
            "version": "v1.1.1",
            "date": "2019-04-18",
            "changes": {
                "refactor": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "changed stdout statements",
                    },
                    {
                        "scope": "schema",
                        "breaking": None,
                        "message": "command logic removed from commitizen base",
                    },
                    {
                        "scope": "info",
                        "breaking": None,
                        "message": "command logic removed from commitizen base",
                    },
                    {
                        "scope": "example",
                        "breaking": None,
                        "message": "command logic removed from commitizen base",
                    },
                    {
                        "scope": "commit",
                        "breaking": None,
                        "message": "moved most of the commit logic to the commit command",
                    },
                ],
                "fix": [
                    {
                        "scope": "bump",
                        "breaking": None,
                        "message": "commit message now fits better with semver",
                    },
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "conventional commit 'breaking change' in body instead of title",
                    },
                ],
            },
        },
        {
            "version": "v1.1.0",
            "date": "2019-04-14",
            "changes": {
                "feat": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "new working bump command",
                    },
                    {"scope": None, "breaking": None, "message": "create version tag"},
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "update given files with new version",
                    },
                    {
                        "scope": "config",
                        "breaking": None,
                        "message": "new set key, used to set version to cfg",
                    },
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "support for pyproject.toml",
                    },
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "first semantic version bump implementaiton",
                    },
                ],
                "fix": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "removed all from commit",
                    },
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "fix config file not working",
                    },
                ],
                "refactor": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "added commands folder, better integration with decli",
                    }
                ],
            },
        },
        {
            "version": "v1.0.0",
            "date": "2019-03-01",
            "changes": {
                "refactor": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "removed delegator, added decli and many tests",
                    }
                ],
                "BREAKING CHANGE": [
                    {"scope": None, "breaking": None, "message": "API is stable"}
                ],
            },
        },
        {"version": "1.0.0b2", "date": "2019-01-18", "changes": {}},
        {
            "version": "v1.0.0b1",
            "date": "2019-01-17",
            "changes": {
                "feat": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "py3 only, tests and conventional commits 1.0",
                    }
                ]
            },
        },
        {
            "version": "v0.9.11",
            "date": "2018-12-17",
            "changes": {
                "fix": [
                    {
                        "scope": "config",
                        "breaking": None,
                        "message": "load config reads in order without failing if there is no commitizen section",
                    }
                ]
            },
        },
        {
            "version": "v0.9.10",
            "date": "2018-09-22",
            "changes": {
                "fix": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "parse scope (this is my punishment for not having tests)",
                    }
                ]
            },
        },
        {
            "version": "v0.9.9",
            "date": "2018-09-22",
            "changes": {
                "fix": [
                    {"scope": None, "breaking": None, "message": "parse scope empty"}
                ]
            },
        },
        {
            "version": "v0.9.8",
            "date": "2018-09-22",
            "changes": {
                "fix": [
                    {
                        "scope": "scope",
                        "breaking": None,
                        "message": "parse correctly again",
                    }
                ]
            },
        },
        {
            "version": "v0.9.7",
            "date": "2018-09-22",
            "changes": {
                "fix": [
                    {"scope": "scope", "breaking": None, "message": "parse correctly"}
                ]
            },
        },
        {
            "version": "v0.9.6",
            "date": "2018-09-19",
            "changes": {
                "refactor": [
                    {
                        "scope": "conventionalCommit",
                        "breaking": None,
                        "message": "moved fitlers to questions instead of message",
                    }
                ],
                "fix": [
                    {
                        "scope": "manifest",
                        "breaking": None,
                        "message": "inluded missing files",
                    }
                ],
            },
        },
        {
            "version": "v0.9.5",
            "date": "2018-08-24",
            "changes": {
                "fix": [
                    {
                        "scope": "config",
                        "breaking": None,
                        "message": "home path for python versions between 3.0 and 3.5",
                    }
                ]
            },
        },
        {
            "version": "v0.9.4",
            "date": "2018-08-02",
            "changes": {
                "feat": [{"scope": "cli", "breaking": None, "message": "added version"}]
            },
        },
        {
            "version": "v0.9.3",
            "date": "2018-07-28",
            "changes": {
                "feat": [
                    {
                        "scope": "commiter",
                        "breaking": None,
                        "message": "conventional commit is a bit more intelligent now",
                    }
                ]
            },
        },
        {
            "version": "v0.9.2",
            "date": "2017-11-11",
            "changes": {
                "refactor": [
                    {
                        "scope": None,
                        "breaking": None,
                        "message": "renamed conventional_changelog to conventional_commits, not backward compatible",
                    }
                ]
            },
        },
        {
            "version": "v0.9.1",
            "date": "2017-11-11",
            "changes": {
                "fix": [
                    {
                        "scope": "setup.py",
                        "breaking": None,
                        "message": "future is now required for every python version",
                    }
                ]
            },
        },
    )


def test_render_changelog(gitcommits, tags, changelog_content):
    parser = defaults.commit_parser
    changelog_pattern = defaults.bump_pattern
    tree = changelog.generate_tree_from_commits(
        gitcommits, tags, parser, changelog_pattern
    )
    result = changelog.render_changelog(tree)
    assert result == changelog_content
