# -*- coding: utf-8 -*-

import logging
import os
import time


logger = logging.getLogger()


def process_photos(rpis, camera):
    """
    Monitors the captured_from_camera list for newly captured photos.
    When a new photos are present it will run arp_ping_macs to remove false positives and then send the photos via Telegram.
    After successfully sendind the photo it will also archive the photo and remove it from the list.
    """
    logger.info("thread running")
    while True:
        if not camera.queue.empty():
            if rpis.state.current == 'armed':
                logger.debug('Running arp_ping_macs before sending photos...')
                rpis.arp_ping_macs()
                time.sleep(2)
                while not camera.queue.empty():
                    if rpis.state.current != 'armed':
                        logger.debug('Stopping photo processing as state is now {0} and clearing queue'.format(rpis.state.current))
                        camera.clear_queue()
                        break
                    photo = camera.queue.get()
                    logger.debug('Processing the photo {0}, state is {1}'.format(photo, rpis.state.current))
                    rpis.state.update_triggered(True)
                    rpis.state.update_triggered_at = time.time()
                    rpis.telegram_send_message('Motion detected')
                    if rpis.telegram_send_file(photo):
                        camera.queue.task_done()
                    rpis.state.update_state('disarmed')
                    if rpis.motion_command:
                        logger.debug('motion_command: {}'.format(rpis.motion_command))
                        os.system(rpis.motion_command)
                    time.sleep(60)  # wait a minute before next alert
                    if rpis.state.current != 'disabled':
                        rpis.state.update_state('armed')
                    logger.debug('Stopping photo processing as state is now {0} and clearing queue'.format(rpis.state.current))
                    camera.clear_queue()
            else:
                logger.debug('Stopping photo processing as state is now {0} and clearing queue'.format(rpis.state.current))
                camera.clear_queue()
        time.sleep(0.1)
