# pixie-dust

Pipeline for the Friday Short Film at ALA 2026

# Purpose

What is my purpose in this project?

- Allow for quicker file transfer that is supported by proper file organisation/management
- Create an streamlined flow of data between each department
- Allow for the creation of tools that could help the project
- Coordinate with Production and provide them with information about all files

# Checklist

## Completed

- [x] Base folder structure complete
- [x] Ability to create assets, shots and sequence folders complete
- [x] Ability to assign assets to users
- [x] UI Tabs Structure finalised - Creation, Assignment, Production, Save, Publish, Import/Reference, Information
- [x] Find a way to not have to change a file each time I use a different setup
  - Another startup file that is ignored by git that provides the sys path first
- [x] Find a way to show what is assigned to a user
- [x] Finalise how data will be passed between software and what software is being used
  - Is it similar to how ALA does it?

## Top Priority

- [ ] Finalise .json structure
  - Finish shot schema
- [ ] Investigate how they created files for shots - which file types and how did wip vs. publish look like
- [ ] Get shots and sequences working for assignment and production
- [ ] Get versioning complete
- [ ] Get saving and publishing complete for Maya
  - Make sure there are changes to be saved before saving
  - Check that it is either "assets" or "sequences" for the first part then check the folder path vs. the name
    - Use the verify_file method
    - This can be changed when the database is made
- [ ] Get Pixie Dust working as a standalone executable (for Production and Art Department)
- Make things snake_case (or at least figure out when I should have items that are camelCase)
- [ ] Further investigate and find a way to import and export data to master production document

## Middle Priority

- [ ] Investigate SQLite as a database system for:
  - Assets / Shots
  - Users
  - Assignments
- [ ] Find a way to assign a user a name on startup
  - Either automatically on first use or first time on every session
  - Could be changed in the information section (?) or some sort of settings section
- [ ] Export in different file types (at least for Maya)
- [ ] Implement USD exports too
- [ ] Get Pixie Dust working for Houdini
- [ ] Get Pixie Dust working for Katana
- [ ] Get Pixie Dust working for Nuke
- [ ] Get USD working
  - Seems like a large change for something that wouldn't be suitable for the time I have

## Low Priority

- [ ] Creation of a Slack/Discord bot to provide updates
- [ ] Thumbnails and turntable for published items

## Guard Rails

- [ ] Clicking only in the UI - Enter could accidently press any button
- [ ] Ensure two people can't manipulate/create files at the same time
  - For now, could be as simple as creating a .lock file and checking if a .lock file exists at edit/creation time

# -------------------------------------------------------------

# Considerations

## Important Note

- Publishes are for review
- Given we have no USD (as for now), all items NEED TO BE FINALISED AND APPROVED before being passed on
  - prop_test_01 prop_test_approved which then becomes prop_test when given to another department

## Top Priority

Get a way to only choose either WIP or published
Get versioning/saving working
Get load versions working
Get publishing working
Get .lock files and gaurd against multiple users saving at the same time (Low priority realistically)
Get shots and sequences working for assignment and production

## Ideas

## Faster Saving

Give a checkbox if they want to receive the window each time they save or not
A notification will still pop up saying they have saved

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
