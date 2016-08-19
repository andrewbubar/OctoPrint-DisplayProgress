# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import pigpio
import os, system, termios, tty, time

RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24

pi = pigpio.pi()

class DisplayProgressPlugin(octoprint.plugin.ProgressPlugin,
                            octoprint.plugin.SettingsPlugin):

	##~~ Settings

	def get_settings_defaults(self):
		return dict(
			message="{bar} {progress:>3}%%"
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			requestspinner=dict(
				displayName="DisplayProgress Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-DisplayProgress",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-DisplayProgress/archive/{target_version}.zip"
			)
		)

	##~~ Progress

	def on_print_progress(self, storage, path, progress):
		if not self._printer.is_printing():
			return
		message = self._settings.get(["message"]).format(progress=progress, storage=storage, path=path, bar=self.__class__._progress_bar(progress))
		self._printer.commands("M117 {}".format(message))

	@classmethod
	def _progress_bar(cls, progress):
		if progress < 20:
			pi.set_PWM_dutycycle(RED_PIN, 204)
			pi.set_PWM_dutycycle(GREEN_PIN, 0)
			pi.set_PWM_dutycycle(BLUE_PIN, 0)
		elif progress >= 20 and progress <= 40
			pi.set_PWM_dutycycle(RED_PIN, 255)
			pi.set_PWM_dutycycle(GREEN_PIN, 128)
			pi.set_PWM_dutycycle(BLUE_PIN, 0)
		elif progress > 40 and progress <= 60
			pi.set_PWM_dutycycle(RED_PIN, 255)
			pi.set_PWM_dutycycle(GREEN_PIN, 255)
			pi.set_PWM_dutycycle(BLUE_PIN, 51)
		elif progress > 60 and progress <= 80
			pi.set_PWM_dutycycle(RED_PIN, 51)
			pi.set_PWM_dutycycle(GREEN_PIN, 51)
			pi.set_PWM_dutycycle(BLUE_PIN, 255)
		elif progress > 80 and progress <= 100
			pi.set_PWM_dutycycle(RED_PIN, 0)
			pi.set_PWM_dutycycle(GREEN_PIN, 204)
			pi.set_PWM_dutycycle(BLUE_PIN, 0)			
		hashes = "#" * int(round(progress / 10))
		spaces = " " * (10 - len(hashes))
		return "[{}{}]".format(hashes, spaces)

__plugin_name__ = "DisplayProgress"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = DisplayProgressPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
pi.stop()
