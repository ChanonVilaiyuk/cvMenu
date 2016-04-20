# -*- coding: utf-8 -*-
''' --------------------------------------------------------------------------
 cv_custom_menu.py : python script / cv_custom_menu.mel : mel wrapper
 --------------------------------------------------------------------------

 DESCRIPTION:
  Create custom menubar attached to Maya Window. Easily manage menu items
  in file structure style. 

 REQUIRES:
  Maya 2012 and newer


 INSTALLATION AND RUNNING:
  This mel script call python module "cvRename.py" 
  Please make sure that both file were put together in scripts directory
  run cvRename();

 AUTHORS:
  Chanon Vilaiyuk
  Copyright ©2016 Chanon Vilaiyuk - All Rights Reserved.
'''


# start here

# import module 
import os, sys, subprocess 
import maya.cmds as mc
import maya.mel as mm 
from functools import partial

# name and menu tree path 
gMainWindow = mm.eval('$tmpVar=$gMainWindow')

# str variables
pathStr = '/'
# separator area 
dividerStr = '===='
dividerLabelStr = '=='
labelSortDivider = '-'

# menu dir variables
cvMenuDir = 'cvMenu'
userAppDir = mc.internalVar(userAppDir = True)
menuDir = pathStr.join([userAppDir, cvMenuDir])



# show menu 
def run(*args) : 
	# iterate menuDir to find all menus
	if not os.path.exists(menuDir) : 
		os.makedirs(menuDir)
		output('Create dir %s' % menuDir)

	menus = listdir(menuDir)

	if menus : 
		for menu in menus : 
			# menu name 
			menuName = '%s_cvMenu' % menu

			# delete menu if exists
			deleteMenu(menuName)

			# menuTree 
			menuTree = pathStr.join([menuDir, menu])

			# main menu 
			mc.menu(menuName, label=menu, tearOff = True, p = gMainWindow)

			# recursion menuTree directory 
			recursionMenu(menuTree)


			# Menu setting menu area
			mc.menuItem(divider = True)

			mc.menuItem(label = 'Menu Setting', subMenu = True)
			mc.menuItem(label = 'Refresh Menu', c = partial(run))
			mc.menuItem(label = 'Create example menus', c = partial(createExampleMenu, menu))
			mc.menuItem(label = 'Show menu tree', c = partial(showMenuTree, menu))
			mc.menuItem(label = 'Remove this menu', c = partial(deleteMenu, menuName))
			mc.setParent( '..', menu=True )



def recursionMenu(path) : 
	''' recursion read all files and directories and create menu items ''' 

	# list all files / folders 
	items = [a for a in os.listdir(path)]

	for eachItem in items : 
		# check if dir or file 

		# if file 
		if os.path.isfile(os.path.join(path, eachItem)) : 
			filePath = os.path.join(path, eachItem)
			command = readCommand(filePath)

			addMenuItem(eachItem, command = command)

		# if dir 
		if os.path.isdir(os.path.join(path, eachItem)) : 
			addMenuItem(eachItem, subMenu = True)

			# recursion only folder that is not divider
			if not isDivider(eachItem) : 
				recursionMenu(os.path.join(path, eachItem))

				mc.setParent( '..', menu=True )



def addMenuItem(name, subMenu=False, command = None) : 
	''' add menu item ''' 

	# get label 
	label = getLabel(name, subMenu)

	# check if divider only 
	if dividerStr in label : 
		mc.menuItem(divider = True)
		return 

	# check if divider with label 
	if dividerLabelStr in label : 
		label = label.replace(dividerLabelStr, '')
		mc.menuItem(divider = True, dividerLabel = label)
		return

	# if sub menu 
	if subMenu : 
		mc.menuItem(subMenu=True, tearOff = True, label=label)

	# if menu item 
	else : 
		# if command in file 
		if command : 
			mc.menuItem(label=label, command = command)

		# if blank file
		else : 
			mc.menuItem(label=label)


def getLabel(label, subMenu) : 
	''' separate sorting digit and label ''' 

	# check for sorted arrange
	# labelSortDivider default is '-'
	if labelSortDivider in label : 
		labelName = label.split(labelSortDivider)[-1]
		sortNumber = label.split(labelSortDivider)[0]
		separatorNum = int(sortNumber[0])

		return labelName

	else : 
		return label

# menu functions ================================

def isDivider(label) : 
	''' check if given label name is a menu label or divider label '''

	if dividerLabelStr in label : 
		return True 

def readCommand(path) : 
	''' open file and read content inside the file '''

	f = open(path, 'r')
	data = f.read()
	f.close()

	return data


def showMenuTree(menu, *args) : 
	''' show menu tree in explorer ''' 

	menuTreeDir = os.path.normpath(pathStr.join([menuDir, menu]))
	subprocess.Popen(r'explorer /select,"%s"' % menuTreeDir)

def deleteMenu(menuName, *args) : 
	''' delete existing menu ''' 

	# delete menu if exists 
	if mc.menu(menuName, exists = True) : 
		mc.deleteUI(menuName)

		# recursion delete 
		deleteMenu(menuName)


def output(message) : 
	print 'cvMenu output: %s' % message

# list file functions ============================

def listdir(path) : 
	dirs = [a for a in os.listdir(path) if os.path.isdir(os.path.join(path, a))]
	return dirs

def listfile(path) : 
	files = [a for a in os.listdir(path) if os.path.isfile(os.path.join(path, a))]
	return files


# create example menu =============================

def createExampleMenu(menu, *args) : 
	# create sub menu 
	createMenu(menu, '00-%sLabel' % dividerLabelStr, fileType = 'dir')
	createMenu(menu, '00-subMenu', fileType = 'dir')
	createMenu(menu, '00-subMenu/00-your command', fileType = 'file')
	createMenu(menu, '01-%s' % dividerStr, fileType = 'file')
	createMenu(menu, '00-your command1', fileType = 'file')
	createMenu(menu, '01-your command2', fileType = 'file')

	output('Create example menu')
	run()
	

def createMenu(menu, label, fileType = 'file') : 
	# menuTreeDir 
	menuTreeDir = pathStr.join([menuDir, menu])

	filePath = pathStr.join([menuTreeDir, label])

	if not os.path.exists(filePath) : 
		if fileType == 'file' : 
			makeFile(filePath)

		if fileType == 'dir' : 
			os.makedirs(filePath)



def makeFile(fileName) : 
	dirname = os.path.dirname(fileName) 

	if not os.path.exists(dirname) : 
		os.makedirs(dirname)

	f = open(fileName, 'w')
	f.close()

	return fileName