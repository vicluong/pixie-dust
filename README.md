# pixie-dust

Pipeline for the Friday Short Film at ALA 2026

## Ideas

### Preferences

How do I assign a preference to each user/computer so that they are automatically recognised as the correct user without input?

Create Settings tab to change user and other stuff

### For Assets Tab in Production Tab:

Current Assignee above WIP and Publish (BUT NOT TREEVIEW)
TreeView containing asset path / ALL WIP Versions / ALL Publish Versions

ALL WIP Versions and Publish Versions in one widget so that only one cell is selected at any one time

Potential in the future for filtering based on type of job/department

## To-Do

### Figure out a way to get users to save in Maya

Either:

- Non-intrusively remind them to save every 10-15 minutes
  - cmds.inViewMessage or cmds.warning
  - To show some change in warning - add what time it was last saved/what time the last reminder was
- Find a good hotkey for saving that DOESN'T affect any current actions
  - Consider Ctrl + Alt + S
- Perhaps both?
- Button for production, button for saving, button for publish and button for import/reference

### Sequence version of assignment

### Conversion of tableview to treeview

- Creation Asset Table
- Creation Shot/Sequence Table
- Assignment Asset Table
- Assignment Shot/Sequence Table

### Save Page and Versioning

### Publish Page and what files am I exporting

### Figuring out how to lock files when someone is publishing or saving

### Figure out the best way to assign a user their name on startup

Either:

- Ask them on startup to pick their name
- Set some sort of preference to store their name
- Find out if they have a preference already to find their name
  - Perhaps something on their computer/account setup will have their name

### Import/Reference

### Generating Information for the Production Crew
