**Description**
<!-- Do not push the release tag until this PR is merged -->
This pull request updates ldcoolp-figshare v0.xx.x -> v0.xx.0

**Check**

<!-- After using this template, check the links in the PR to ensure they resolve and replace `../../` with `../tree/main/` in any broken link. -->
- [ ] Title and description have been updated.
- [ ] Verified the correct branch is being merged by checking the text immediately below the PR title.
- [ ] Updated version in [`setup.py`](../../setup.py)
- [ ] Updated version in [`ldcoolp_figshare/__init__.py`](../../ldcoolp_figshare/__init__.py)
- [ ] Updated version in ReadTheDocs [`conf.py`](../../docs/source/conf.py)

**Begin a new release**
:warning: Do not publish the release until this PR is merged :warning:
- [ ] Go to the [New Release](../releases/new) page
- [ ] In the `Choose a tag` dropdown, enter a new tag name corresponding to the new version. E.g., `v1.0.1`. Then click "Create new tag on publish"
- [ ] The `Target` should be the main or master branch.
- [ ] Click the `Generate release notes` button. Review the notes for accuracy
- [ ] Save the release as Draft.

**Update Documentation in the Branch**
- [ ] Copy the generated release notes from the previous step to the top of `CHANGELOG.md`
- [ ] Update `README.md` (if needed)
- [ ] [ReadTheDocs files](../../docs/source/). Check and update the appropriate sections in the .rst files as needed

**Release**
- [ ] Merge this PR
- [ ] Return to [Releases](../releases) and publish the draft release.