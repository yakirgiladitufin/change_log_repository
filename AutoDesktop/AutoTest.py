import AutoDesktop

AutoDesktop.keyboard_press('winleft')
AutoDesktop.keyboard_type('pc')
AutoDesktop.keyboard_press('enter')
AutoDesktop.keyboard_multiPress('winleft up')

D_driver = AutoDesktop.UIElem("Test_imgs/C_drive.png")
if not D_driver.find():
	AutoDesktop.log('Cannot found C_driver')
else:
	D_driver.click('Double')

	new_folder = AutoDesktop.UIElem("Test_imgs/new_folder.png")
	if not new_folder.find():
		AutoDesktop.log('Cannot found new_folder')
	else:
		new_folder.click('Single')

		AutoDesktop.keyboard_type(type_write='test folder',speed=0.1)
		AutoDesktop.keyboard_press('enter')

		AutoDesktop.keyboard_press(['up','up','up','up','up'])
		##
		test_folder = AutoDesktop.UIElem("Test_imgs/test_folder.png")
		if not test_folder.find():
			AutoDesktop.log('Cannot found test_folder')
		else:
			test_folder.click('Right')
			AutoDesktop.keyboard_press(['up','up','up'])
			AutoDesktop.keyboard_multiPress('shift enter')
			AutoDesktop.keyboard_press('enter')

			test_folder = AutoDesktop.UIElem("Test_imgs/test folder.png", attempts = 1)
			test_folder_exists = test_folder.find()
			if test_folder_exists:
				AutoDesktop.log('Cannot Delete \'test folder\'')
			else:
				AutoDesktop.log('Delete \'test folder\'')
				AutoDesktop.log('Test Passed')