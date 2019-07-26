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
import os
import re
import shutil

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

        self.ui.output_btn.clicked.connect(self._publish_to_shotgun)
        self.ui.farm_btn.clicked.connect(self._publish_to_shotgun)
    
    

    def _set_frame(self):
        start_time = NodegraphAPI.NodegraphGlobals.GetWorkingInTime()
        end_time = NodegraphAPI.NodegraphGlobals.GetWorkingOutTime()

        self.ui.start_frame.setText(str(start_time))
        self.ui.end_frame.setText(str(end_time))
        

    def _set_select_node(self,eventType=None,eventID=None,node=None):
        
        msg = []
        self.selected_nodes = []

        nodes =  NodegraphAPI.GetAllSelectedNodes()
        for node in nodes:
            if node.getType() == "Render":
                msg.append(node.getName())
                self.selected_nodes.append(node)
        msg = ",".join(msg)        
        self.ui.sel_node.setText(msg)
        return 



    def _render(self):
        import os
        
        file_name = FarmAPI.GetKatanaFileName()
        
        #tmp_file = os.path.join("/tmp",file_name.split("/")[-1])
        #KatanaFile.Save(tmp_file)
        
        
        if os.environ['REZ_KATANA_VERSION'] == "3.1v2":
            command = ['mate-terminal','-x','rez-env','katana-3.1v2','renderman-22','usd-19.03',"yeti",'--','katana']
        else:
            command = ['mate-terminal','-x','rez-env','katana-2.6v4','renderman-21.8','usd-19.03','yeti-2.2.9','--','katana']

        temp_file = self._get_temp_file(str(file_name))
        if not os.path.exists(os.path.dirname(temp_file)):
            os.makedirs(os.path.dirname(temp_file))
        status = shutil.copyfile(file_name,temp_file)
        
        
        for node in self.selected_nodes:

            command.append("--batch")
            command.append("--katana-file=%s"%temp_file)
            command.append("--render-node=%s"%node.getName())
            command.append(str('--t=%s-%s'%(self.ui.start_frame.text(),self.ui.end_frame.text())))
        
        

            subprocess.Popen(command)
        self.close()
        return
    
    def _get_temp_file(self,file_name):
        temp = "/"
        file_dirs = os.path.dirname(file_name).split("/")
        filename = "."+os.path.basename(file_name)
        file_dirs.append(filename)
        return temp.join(file_dirs)

        

    
    def _render_to_farm(self):
        
        import tractor.api.author as author
        
        start_frame = int(self.ui.start_frame.text())
        end_frame = int(self.ui.end_frame.text())
        file_name = FarmAPI.GetKatanaFileName()

        

        temp_file = self._get_temp_file(str(file_name))
        if not os.path.exists(os.path.dirname(temp_file)):
            os.makedirs(os.path.dirname(temp_file))
        status = shutil.copyfile(file_name,temp_file)

        for node in self.selected_nodes:
            job = author.Job()
        #job.title = '[Katana]' + file_name.split(".")[0].split("/")
            job.service = "Linux64"
            job.priority = 50
        
            file_title = file_name.split(".")[0].split("/")[-1]
            project_name = self._app.context.project['name']
            user_name = self._app.context.user['name']
            user_id = os.environ['USER']
            select_node = str(node.getName())
        


            temp = "] ["
            title = []
            title.append(user_name)
            title.append(project_name)
            title.append(file_title)
            title.append(select_node)
            title.append("%d - %d"%(start_frame,end_frame))
            title = temp.join(title)
            title = "["+title+"]"
            job.title = str(title)

            for frame in range(start_frame,end_frame+1):
                task = author.Task(title = str(frame))

                if os.environ['REZ_KATANA_VERSION'] == "3.1v2":
                    command = ['rez-env','katana-3.1v2','renderman-22','usd-19.03','yeti','--','katana']
                else:
                    command = ['rez-env','katana-2.6v4','renderman-21.8','usd-19.03','yeti-2.2.9','--','katana']
                command.append("--batch")
                command.append("--katana-file=%s"%temp_file)
                command.append("--render-node=%s"%node.getName())
                command.append(str("--t=%d-%d"%(frame,frame)))
                command = author.Command(argv=command)
                task.addCommand(command)
                job.addChild(task)
        
            job.spool(hostname="10.0.20.80",owner=user_id)


        self.close()
        return

    def _publish_to_shotgun(self):
        
        if not self.ui.sg_check.isChecked():
            return
        
        
        context = self._app.context
        user = context.user
        
        for node in self.selected_nodes:
            if node.getName().find("_bty") == -1:
                continue
            primary_path = self._get_publish_file_info(node)    
            version = self._get_version()

            if sgtk.util.find_publish(context.tank,[primary_path]):
                continue

            publish_data = {
                "tk": context.tank,
                "context": context,
                "path": primary_path,
                "name": context.entity['name'] + "_" + node.getName(),
                "created_by": context.user,
                "version_number": version,
                #"thumbnail_path": item.get_thumbnail_as_path(),
                "published_file_type": "Rendered Image",
                #"dependency_paths": publish_dependencies
                }

            sgtk.util.register_publish(**publish_data)
        

    
    def _get_publish_file_info(self,node):
        index = 0
        while 1:
            if node.getParameter("outputs").getChild("allOutputNames").getChildByIndex(index).getValue(0) == 'primary':
                break
            else:
                index = index + 1
        return node.getParameter("outputs").getChild("locations").getChildByIndex(index).getValue(0)
    
    def _get_version(self):
        
        file_name = FarmAPI.GetKatanaFileName()
        return int(filter(str.isdigit,re.search("v\d+",file_name).group()))
    
    def closeEvent(self,event):
        
        Utils.EventModule.UnregisterEventHandler(self._set_select_node, 'node_setSelected')
    
