from AutoDesktop import *

keyboard_press("winleft")
keyboard_type("pc",0)
keyboard_press("enter")
C_driver = UIElem("C:/AutoDesktop/Test_imgs/C_driver.png",3,1)
C_driver_clicked = C_driver.click("Double")
if not(C_driver_clicked):
	log("Cannot clicked on C_driver")
else:
	new_folder = UIElem("C:/AutoDesktop/Test_imgs/new_folder.png",3,1)
	new_folder_clicked = new_folder.click('Single')
	if not(new_folder_clicked):
		log("Cannot clicked on new_folder")
	else:
		keyboard_type("test_folder",0)
		keyboard_press("enter")
		keyboard_press("up")
		keyboard_press("up")
		keyboard_press("up")
		keyboard_press("up")
		keyboard_press("up")
		test_folder = UIElem("C:/AutoDesktop/Test_imgs/test_folder.png",3,1)
		test_folder_clicked = test_folder.click("Right")
		if not(test_folder_clicked):
			log("Cannot found test_folder")
			keyboard_press("down")
			keyboard_press("down")
			keyboard_press("down")
			keyboard_press("down")
			keyboard_press("down")
			keyboard_press("delete")
		if(test_folder_clicked):
			keyboard_press("up")
			keyboard_press("up")
			keyboard_press("up")
			keyboard_press("enter")
			keyboard_press("enter")
		test_folder = UIElem("C:/AutoDesktop/Test_imgs/test_folder.png",1,1)
		test_folder_exists = test_folder.find()
		if(test_folder_exists):
			log("Cannot Delete \'test folder\'")
		else:
			log("'Delete \'test folder\''")
			log("test PASSED")
