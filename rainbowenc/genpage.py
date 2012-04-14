#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_header():
    return """
    <div id="header">
      <div id="headerlogo">
        <a title="www.doorsolutions.cn" href="http://www.doorsolutions.cn" target="_blank"><img src="/static/header_logo.png" alt="logo" /></a>
      </div>
      <div id="headerrlogo">
        <div class="hostname">
          <span>http://www.doorsolutions.cn&nbsp;</span>
        </div>
      </div>
    </div>"""

def get_headernavbar():
    return """
    <div id="headernavbar">
      <ul id="navbarmenu">
        <li>
	  <a href="recorderctl.html" onmouseover="mopen('recorder')" onmouseout="mclosetime()">""" + _("Recorder") + """</a>
          <div id="recorder" onmouseover="mcancelclosetime()" onmouseout="mclosetime()">
            <a href="recorderctl.html" target="_self" title="Recorder Control">""" + _("Recorder Control") + """</a>
            <a href="recorderfile.html" target="_blank" title="Recorder File Manager">""" + _("Recorder File Manager") + """</a>
          </div>
        </li>
        <li>
	  <a href="rainbow.html" onmouseover="mopen('system')" onmouseout="mclosetime()">""" + _("System") + """</a>
          <div id="system" onmouseover="mcancelclosetime()" onmouseout="mclosetime()">
            <a href="changepass.html" target="_self" title="Change Password">""" + _("Change Passsword") + """</a>
            <a href="selectlang.html" target="_self" title="Select Language">""" + _("Select Language") + """</a>
            <a href="netconfigure.html" target="_self" title="LAN Management">""" + _("LAN Management") + """</a>
            <!--a href="system_backup.php" target="_self" title="Backup/Restore">Backup/Restore</a-->
            <!--a href="system_defaults.php" target="_self" title="Factory defaults">Factory defaults</a-->
            <span class="tabseparator">&nbsp;</span>
            <a href="reboot.html" target="_self" title="Reboot">""" + _("Reboot") + """</a>
            <a href="shutdown.html" target="_self" title="Shutdown">""" + _("Shutdown") + """</a>
            <a href="logout" target="_self" title="Logout">""" + _("Logout") + """</a>
          </div>
        </li>
        <!--li>
          <a href="rainbow.html" onmouseover="mopen('advanced')" onmouseout="mclosetime()">Advanced</a>
          <div id="advanced" onmouseover="mcancelclosetime()" onmouseout="mclosetime()">
            <a href="system_edit.php" target="_self" title="File Editor">File Editor</a>
            <a href="quixplorer" target="_blank" title="File Manager">File Manager</a>
            <span class="tabseparator">&nbsp;</span>
            <a href="exec.php" target="_self" title="Command">Command</a>
          </div>
        </li-->
        <li>
	  <a href="rainbow.html" onmouseover="mopen('status')" onmouseout="mclosetime()">""" + _("Status") + """</a>
          <div id="status" onmouseover="mcancelclosetime()" onmouseout="mclosetime()">
            <a href="rainbow.html" target="_self" title="System">""" + _("System") + """</a>
            <a href="channelstatus.html" target="_self" title="Encoder">""" + _("Encoder Channel") + """</a>
            <a href="netstatus.html" target="_self" title="Network">""" + _("Network Interface") + """</a>
          </div>
        </li>
        <li>
          <a href="rainbow.html" onmouseover="mopen('help')" onmouseout="mclosetime()">""" + _("Help") + """</a>
          <div id="help" onmouseover="mcancelclosetime()" onmouseout="mclosetime()">
            <a href="http://www.doorsolutions.cn" target="_blank" title="Information &amp; Manual">""" + _("Information &amp; Manual") + """</a>
            <a href="http://www.doorsolutions.cn" target="_self" title="Release notes">""" + _("Release notes") + """</a>
            <a href="http://www.doorsolutions.cn" target="_self" title="License & Credits">""" + _("License & Credits") + """</a>
            <a href="http://www.doorsolutions.cn" target="_blank" title="Donate">""" + _("Donate") + """</a>
          </div>
        </li>
      </ul>
      <div style="clear:both"></div>
    </div>"""

def get_footer():
    return """
    <div id="pagefooter">
      <span>
        <a title="www.doorsolutions.cn" href="http://www.doorsolutions.cn" target="_blank">RainBOW</a>
         """ + _("&copy; 2010-2010 by DOOR Solutions. All rights reserved.") + """
        <a href="http://www.tibet.com/" class="tblnk">&nbsp;</a>
      </span>
    </div>"""
