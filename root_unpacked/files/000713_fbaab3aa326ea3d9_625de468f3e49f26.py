import dbg
import app
import localeInfo
import wndMgr
import systemSetting
import mouseModule
import networkModule
import constInfo
import musicInfo
import net


if constInfo.ENABLE_PASTE_FEATURE:
	from ui import EnablePaste as ui_EnablePaste
	ui_EnablePaste(True)

def RunApp():
	mouseModule.mouseController = mouseModule.CMouseController()

	musicInfo.LoadLastPlayFieldMusic()

	app.SetHairColorEnable(constInfo.HAIR_COLOR_ENABLE)
	app.SetArmorSpecularEnable(constInfo.ARMOR_SPECULAR_ENABLE)
	app.SetWeaponSpecularEnable(constInfo.WEAPON_SPECULAR_ENABLE)

	app.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())

	try:
		app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	except RuntimeError as msg:
		msg = str(msg)
		if "CREATE_DEVICE" == msg:
			dbg.LogBox("Sorry, Your system does not support 3D graphics,\r\nplease check your hardware and system configeration\r\nthen try again.")
		else:
			dbg.LogBox("Metin2.%s" % msg)
		return

	app.SetCamera(1500.0, 30.0, 0.0, 180.0)


	if not mouseModule.mouseController.Create():
		return

	mainStream = networkModule.MainStream()
	mainStream.Create()
	mainStream.SetLogoPhase()

	app.Loop()

	mainStream.Destroy()

	if mouseModule.mouseController:
		mouseModule.mouseController.Destroy()
		mouseModule.mouseController = None

RunApp()

