# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


import subprocess
import sys

import sgtk


from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from sgtk import TankError



from Katana import NodegraphAPI
from Katana import Utils
from Katana import FarmAPI
from Katana import KatanaFile



def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system. 
    
    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Output", app_instance, AppDialog)
    


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self)
        
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        self._app = sgtk.platform.current_bundle()

        
        self._set_frame()
        self._set_select_node()
        
        #callback
        Utils.EventModule.RegisterEventHandler(self._set_select_node, 'node_setSelected')

        #self.ui.tail_lineedit.textChanged.connect(self._edit_tail)
        self.ui.output_btn.clicked.connect(self._render)
        self.ui.farm_btn.clicked.connect(self._render_to_farm)
    
    

    def _set_frame(self):
        start_time = NodegraphAPI.NodegraphGlobals.GetWorkingInTime()
        end_time = NodegraphAPI.NodegraphGlobals.GetWorkingOutTime()

        self.ui.start_frame.setText(str(start_time))
        self.ui.end_frame.setText(str(end_time))
        

    def _set_select_node(self,eventType=None,eventID=None,node=None):
        
        if not node:
            node =  NodegraphAPI.GetAllSelectedNodes()[0]
        self.ui.sel_node.setText(node.getName())
        return 

    def _render(self):
        import os
        
        file_name = FarmAPI.GetKatanaFileName()
        
        #tmp_file = os.path.join("/tmp",file_name.split("/")[-1])
        #KatanaFile.Save(tmp_file)


        command = ['mate-terminal','rez-env','katana-3.1.2','renderman-22','usd','--','katana']
        
        command.append("--batch")
        command.append("--katana-file=%s"%file_name)
        command.append("--render-node=%s"%self.ui.sel_node.text())
        command.append(str("--t=%s-%s"%(self.ui.start_frame.text(),self.ui.end_frame.text())))

        subprocess.Popen(command)
        self.close()
        return
    
    def _render_to_farm(self):
        
        import tractor.api.author as author
        
        start_frame = int(self.ui.start_frame.text())
        end_frame = int(self.ui.end_frame.text())
        file_name = FarmAPI.GetKatanaFileName()
        
        job = author.Job()
        job.title = '[Katana]' + file_name.split(".")[0]
        job.service = "Linux64"
        job.priority = 50
        
        for frame in range(start_frame,end_frame+1):
            task = author.Task(title = str(frame))
            command = ['rez-env','katana-3.1v2','renderman-22','usd','--','katana']
            command.append("--batch")
            command.append("--katana-file=%s"%file_name)
            command.append("--render-node=%s"%self.ui.sel_node.text())
            command.append(str("--t=%d-%d"%(frame,frame)))
            command = author.Command(argv=command)
            task.addCommand(command)
            job.addChild(task)
        
        job.spool(hostname="10.0.0.80",owner="west")



        



    
    def closeEvent(self,event):
        
        Utils.EventModule.UnregisterEventHandler(self._set_select_node, 'node_setSelected')
    
