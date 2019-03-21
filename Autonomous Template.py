import sys
import tarfile, os
import json
import base64
import io
import pcpp
import time
import platform
from io import StringIO
import argparse
import subprocess
python VCS4CMD.py -po

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--preprocess", help="Pack with preprocessor", action="store_true")
parser.add_argument("-r", "--repack", help="Pack without preprocessor", action="store_true")
parser.add_argument("-u", "--unpack", help="Unpack (requires file parameter)", action="store_true")
parser.add_argument("--file", help="Specify file name for unpacking")
parser.add_argument("-o", "--open", help="Opens file in VCS after it is processed. VCS must be installed.", action="store_true")
parser.add_argument("-t", "--template", help="Generate template files for editing and use with NotVCS", action="store_true")
parser.add_argument("-l", "--upload", help="Automatically compile and upload program to robot. Requires Vex Coding Studio, PROSv5, and GnuWin32 make to be used.", action="store_true")
args = parser.parse_args()
#print(type(args))

def unpackArgs() :
	arguments = {}
	tracker = ""
	for arg in sys.argv:
		if(arg.startswith("--")):
			tracker = arg[2:]
		elif(tracker == ""):
			continue
		else:
			arguments[tracker] = arg
			tracker = ""
	return arguments 

# if __name__ == "__main__":
	# args = unpackArgs()
	
#if __name__ == "__main__" and ():
#	print("NotVCS.py Help Menu\n\nOptions:\n--help me - Shows help menu\n--mode <unpack/repack> - Specify whether to unpack or repack a .vex file\n--file <file name> - Specify the name of your file")
	
if __name__ == "__main__" and args.template:
	print("Generating template files...")
	if not os.path.exists("unpacked/source/"):
		try:
			os.makedirs("unpacked/source/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	
	if not os.path.exists("unpacked/source/main.cpp"):
		with open("unpacked/source/main.cpp", "w") as main:
			main.write("""
#include "robot-config.h"
/*---------------------------------------------------------------------------

       WalshBots 9791 unified competition template                              
       Authors:  Liam Donovan, CJ Crocker
       Contributors:  
                James Pearman - Brain Auton Button Selector
                Pascal Chesnais - multimotor abstractions

                Modification History:
                1/5/2019 - prc - instructional version...
  ---------------------------------------------------------------------------*/
vex::competition    Competition;



//IMPORTANT: 
//IGNORE THE CODE BELOW UNTIL YOU GET TO THE PRE_AUTON AND AUTONOMOUS CODE WHERE YOU WILL INPUT YOUR CODE
//DON'T CHANGE ANYTHING ELSE



int   autonomousSelection = -1;


typedef struct _button {
    int    xpos;
    int    ypos;
    int    width;
    int    height;
    bool   state;
    vex::color offColor;
    vex::color onColor;
    const char *label;
} button;

button buttons[] = {
    {   30,  30, 60, 60,  false, 0xE00000, 0x0000E0, "Ally" },
    {  150,  30, 60, 60,  false, 0x303030, 0xD0D0D0, "Start" },
    {  270,  30, 60, 60,  false, 0x303030, 0xF700FF, "Park" },
    {  390,  30, 60, 60,  false, 0x303030, 0xDDDD00, "Shoot" },
    {   30, 150, 60, 60,  false, 0x404040, 0xC0C0C0, "4-" },
    {  150, 150, 60, 60,  false, 0x404040, 0xC0C0C0, "5-" },
    {  270, 150, 60, 60,  false, 0x404040, 0xC0C0C0, "6-" },
    {  390, 150, 60, 60,  false, 0x404040, 0xC0C0C0, "7-" }
};

void displayButtonControls( int index, bool pressed );

int
findButton(  int16_t xpos, int16_t ypos ) {
    int nButtons = sizeof(buttons) / sizeof(button);

    for( int index=0;index < nButtons;index++) {
      button *pButton = &buttons[ index ];
      if( xpos < pButton->xpos || xpos > (pButton->xpos + pButton->width) )
        continue;

      if( ypos < pButton->ypos || ypos > (pButton->ypos + pButton->height) )
        continue;

      return(index);
    }
    return (-1);
}

void
initButtons() {
    int nButtons = sizeof(buttons) / sizeof(button);

    for( int index=0;index < nButtons;index++) {
      buttons[index].state = false;
    }
}

void
userTouchCallbackPressed() {
    int index;
    int xpos = Brain.Screen.xPosition();
    int ypos = Brain.Screen.yPosition();

    if( (index = findButton( xpos, ypos )) >= 0 ) {
      displayButtonControls( index, true );
    }

}

void
userTouchCallbackReleased() {
    int index;
    int xpos = Brain.Screen.xPosition();
    int ypos = Brain.Screen.yPosition();

    if( (index = findButton( xpos, ypos )) >= 0 ) {
      // clear all buttons to false, ie. unselected
      //      initButtons(); 

      // now set this one as true
      if( buttons[index].state == true) {
      buttons[index].state = false; }
      else    {
      buttons[index].state = true;}

      // save as auton selection
      autonomousSelection = index;

      displayButtonControls( index, false );
    }
}

void
displayButtonControls( int index, bool pressed ) {
    vex::color c;
    Brain.Screen.setPenColor( vex::color(0xe0e0e0) );

    for(int i=0;i<sizeof(buttons)/sizeof(button);i++) {

      if( buttons[i].state )
        c = buttons[i].onColor;
      else
        c = buttons[i].offColor;

      Brain.Screen.setFillColor( c );

      // button fill
      if( i == index && pressed == true ) {
        Brain.Screen.drawRectangle( buttons[i].xpos, buttons[i].ypos, buttons[i].width, buttons[i].height, c );
      }
      else
        Brain.Screen.drawRectangle( buttons[i].xpos, buttons[i].ypos, buttons[i].width, buttons[i].height );

      // outline
      Brain.Screen.drawRectangle( buttons[i].xpos, buttons[i].ypos, buttons[i].width, buttons[i].height, vex::color::transparent );

// draw label
      if(  buttons[i].label != NULL )
        Brain.Screen.printAt( buttons[i].xpos + 8, buttons[i].ypos + buttons[i].height - 8, buttons[i].label );
    }
}

void shootPuncher()
{
    //Insert puncher code
}

void lowerFlipper(){
    Flipper.rotateTo(-250,rotationUnits::deg,100,velocityUnits::pct, false);

}
void raiseFlipper(){
    Flipper.rotateTo(0,rotationUnits::deg,100,velocityUnits::pct, false);

}

/* WalshBot Multimotor Drive functions
    void driveSetVelocity (int ) - initializes velocity for all drive motors percent
    void driveRotateFor( float) - allows robot to move forward # of rotations (negative number opposite)
    void driveTurnFor( float) - spin robot about center with drives turning opposite directions 
    void driveTurnDegrees( float) - spin robot about center with drives turning opposite directions 
    */
void driveSetVelocity( double speed)
{
    Leftfront.setVelocity(speed, vex::velocityUnits::pct); 
    Rightfront.setVelocity(speed, vex::velocityUnits::pct);
    Leftback.setVelocity(speed, vex::velocityUnits::pct); 
    Rightback.setVelocity(speed, vex::velocityUnits::pct); 
}

void driveRotateFor(float count)
{
    driveSetVelocity(80.0);    // set the drive velocity for all four motors
    Leftfront.rotateFor(count, rotationUnits::rev,false);
    Leftback.rotateFor(count, rotationUnits::rev,false);
    Rightback.rotateFor(count, rotationUnits::rev,false);
    Rightfront.rotateFor(count, rotationUnits::rev);       // block until complete
    task::sleep(50);   
}

void driveDistance(float distance)
{
    // tested distance for 5 revolutions - travelled 66", so each revolution travels 12.2"
    // so to convert inches to revolutions divide the distance by 12.2
    driveRotateFor(distance*0.082);
}

void driveTurnFor(float count)
{
    Leftfront.rotateFor(-1.0*count, rotationUnits::rev,false);
    Leftback.rotateFor(-1.0*count, rotationUnits::rev,false);
    Rightback.rotateFor(count, rotationUnits::rev,false);
    Rightfront.rotateFor(count, rotationUnits::rev);  // block until complete
    task::sleep(50);   
}

void driveTurnDegrees(float degrees)
{
    float rotdegree = 0.82/90;

    driveSetVelocity(40.0);    // turn more slowly to avoid overshoot

    driveTurnFor( degrees * rotdegree );
 
}

void driveTurnLeftDegrees(float degrees)    // counter clockwise - so negative degrees
{
    driveTurnDegrees( 1.0 * degrees);       
}

void driveTurnRightDegrees(float degrees)   // clockwise
{
    driveTurnDegrees(-1.0 * degrees);
}





//IMPORTANT:
//INPUT YOUR CODE INTO THE AUTONOMOUS CODE WHERE IT TELLS YOU TO


void pre_auton( void ) {
   //Put pre_autonomous functions here 
}

void autonomous( void ) {

    bool allianceBlue = buttons[0].state;
    bool startTileFar = buttons[1].state;
    bool doPark = buttons[2].state;
    bool shootPreload = buttons[3].state;
/*
    Buttons explanation:
    if(allianceBlue) means that this is if you are playing for the blue alliance. This is useful for the turns that are mirrored between the red and blue alliance.
    if(!allianceBlue) means that you're with the red alliance.
    
    How to use this code:
    
    if(allianceBlue){ 
    
    Input your code for the blue alliance here
    
    }
    else{
    
    Input your code for the red alliance here. It should be the opposite of the code for the blue alliance
    
    
    if(doPark) means that you want to park
    if(!doPark) means you don't want to park
    
    How to use this code:
    
    if(doPark){ 
    
    Parking code goes here
    
    }
    else{
    
    vex::task::yield()
    
    }
    
    
    if(shootPreload) means you want to shoot preload
    if(!shootPreload) means you don't want to shoot preload
    
    How to use this code:
    
    if(shootPreload){ 
    
    shootPuncher(); or your punching code
    
    }
    
    
*/  
    if(!startTileFar){  // Starting tile nearest to the flags/net
       
        //Insert code for the tile near the flags here
       
        }              
    }

    else // far from flag/net starting tile
    {

      //Insert vode for the tile far from the flags here
       
        }              
    }

}







/* 
IMPORTANT:
Don't change the code below!
         |
         |
         v                  */
int main() {
    pre_auton();
    Competition.autonomous( autonomous );
    Brain.Screen.pressed( userTouchCallbackPressed );
    Brain.Screen.released( userTouchCallbackReleased );
    Brain.Screen.setFillColor( vex::color(0x404040) );
    Brain.Screen.setPenColor( vex::color(0x404040) );
    Brain.Screen.drawRectangle( 0, 0, 480, 120 );
    Brain.Screen.setFillColor( vex::color(0x808080) );
    Brain.Screen.setPenColor( vex::color(0x808080) );
    Brain.Screen.drawRectangle( 0, 120, 480, 120 );
    displayButtonControls( 0, false );
    while(1) {
        if( !Competition.isEnabled() )
            Brain.Screen.setFont(fontType::mono40);
        Brain.Screen.setFillColor( vex::color(0xFFFFFF) );

        Brain.Screen.setPenColor( vex::color(0xc11f27));
        Brain.Screen.printAt( 0,  135, " Autonomous Program " );
        this_thread::sleep_for(10);
    }
}

      
			""")
		with open("unpacked/vexfile_info.json", "w") as vfinfo:
			vfinfo.write("""
{"title": "NotVCS Program", "description": "A short description of your project", "version": "0.0.1", "icon": "USER000x.bmp", "competition": false, "device": {"slot": 1, "type": "vexV5"}, "language": {"name": "c++"}, "components": []}
			""")
		with open("unpacked/source/robot-config.h","w") as rcfg:
			rcfg.write("vex::brain Brain;")
elif __name__ == "__main__" and args.unpack:
	try:
		assert args.file != None
	except:
		raise Exception("You must specify a file!")
	if not os.path.exists("unpacked/source/"):
		try:
			os.makedirs("unpacked/source/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	vexFile = args.file
	print("Reading from file %s" % vexFile)
	tar = tarfile.open(vexFile, mode="r:*")
	for containedFile in tar.getmembers():
		cFile = tar.extractfile(containedFile)
		dataJson = cFile.read()
	#print(dataJson.decode())
	dataExtracted = json.loads(dataJson)
	
	files = dataExtracted.pop('files', None)
	if files == None:
		raise Exception("Invalid file")
	
	with open('unpacked/vexfile_info.json', 'w', newline='') as csvFile:
		csvFile.write(json.dumps(dataExtracted))
			
	for fileName in files:
		with open("unpacked/source/" + fileName, "w") as el_file:
			notb64 = base64.b64decode(files[fileName])
			el_file.write(notb64.decode('utf-8'))

elif __name__ == "__main__" and args.repack:
	with open('unpacked/vexfile_info.json', 'r') as csv_file:
		vfi = json.loads(csv_file.read())
	files = {}
	for fileName in os.listdir('unpacked/source/'):
		e = open("unpacked/source/" + fileName, "r")
		files[fileName] = base64.b64encode(e.read().encode()).decode('utf-8')
		e.close()
		
	vfi["files"] = files
	fn = vfi["title"]
	jvfi = json.dumps(vfi)
	#jvfi = jvfi.replace("'", "\"")
	abuf = io.BytesIO()
	abuf.write(jvfi.encode())
	abuf.seek(0)
	tar = tarfile.open(fn + ".vex", mode="w:")
	jsonfiletarinfo = tarfile.TarInfo(name="___ThIsisATemPoRaRyFiLE___.json")
	jsonfiletarinfo.size = len(abuf.getbuffer())
	tar.addfile(tarinfo=jsonfiletarinfo,fileobj=abuf)

elif __name__ == "__main__" and args.upload:

	if not os.path.exists("build/"):
		try:
			os.makedirs("build/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
				
	if not os.path.exists(os.path.expanduser('~') + "/AppData/local/VEX Coding Studio/VEX Coding Studio/sdk/user/"):
		raise Exception("Vex Coding Studio must be installed")
	if not os.path.exists(os.path.expanduser('~') + "\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\prosv5.exe"):
		raise Exception("With this version, PROS 3 must be installed. This may be changed in a future release")
	if not os.path.exists("C:\\Program Files (x86)\\GnuWin32\\bin\\make.exe"):
		raise Exception("GNUWin32 make must be installed")
	
	sys.stdout.flush()
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	p = pcpp.cmd.CmdPreprocessor(["pcpp", "unpacked/source/main.cpp", "--line-directive", "--passthru-unfound-includes"])
	sys.stdout = old_stdout
	pCont = mystdout.getvalue()
	#print(vars(p))
	pCont.replace('\n'*2, '\n')
	topMessage = "/***********************************************************************************\nThis code was generated from multiple source files using NotVCS, by AusTIN CANs 2158\n https://github.com/dysproh/notvcs \n***********************************************************************************/\n"
	uCont = topMessage + pCont
	#sys.stdout.flush()
	#int("h" + preprocessedFile.read())
	#print(pCont)
	#jvfi = jvfi.replace("'", "\"")
	abuf = open(os.path.expanduser('~') + "/AppData/local/VEX Coding Studio/VEX Coding Studio/sdk/user/main.cpp", "w")
	abuf.write(uCont)
	os.chdir (os.path.expanduser('~').replace("\\", "/") + '/AppData/local/VEX Coding Studio/VEX Coding Studio/sdk/user/')
	os.system('C:\\"Program Files (x86)"\\GnuWin32\\bin\\make.exe -f makefile-cmd clean')
	os.system('C:\\"Program Files (x86)"\\GnuWin32\\bin\\make.exe -f makefile-cmd cxx_bin')
	os.system('prosv5 upload cxx.bin')

	


elif __name__ == "__main__" and args.preprocess:

	if not os.path.exists("build/"):
		try:
			os.makedirs("build/")
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	sys.stdout.flush()
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	p = pcpp.cmd.CmdPreprocessor(["pcpp", "unpacked/source/main.cpp", "--line-directive", "--passthru-unfound-includes"])
	sys.stdout = old_stdout
	pCont = mystdout.getvalue()
	#print(vars(p))
	pCont.replace('\n'*2, '\n')
	topMessage = "/***********************************************************************************\nThis code was generated from multiple source files using NotVCS, by AusTIN CANs 2158\n https://github.com/dysproh/notvcs \n***********************************************************************************/\n"
	uCont = topMessage + pCont
	#sys.stdout.flush()
	#int("h" + preprocessedFile.read())
	#print(pCont)
	files = {"main.cpp": base64.b64encode(uCont.encode()).decode('utf-8'), "robot-config.h": ""}
	config = open("unpacked/vexfile_info.json", "r")
	ufi = config.read()
	config.close()
	vfi = {}
	vfi = json.loads(ufi)
	#print(type(vfi))
	vfi["files"] = files
	fn = vfi["title"]
	fn = fn.replace(" ", "-")
	jvfi = json.dumps(vfi)
	#jvfi = jvfi.replace("'", "\"")
	abuf = io.BytesIO()
	abuf.write(jvfi.encode())
	abuf.seek(0)
	tar = tarfile.open(fn + ".vex", mode="w:")
	jsonfiletarinfo = tarfile.TarInfo(name="___ThIsisATemPoRaRyFiLE___.json")
	jsonfiletarinfo.size = len(abuf.getbuffer())
	tar.addfile(tarinfo=jsonfiletarinfo,fileobj=abuf)
	tar.close()
	if args.open:
		try:
			if platform.system() == "Windows":
				retcode = subprocess.call("start " + fn + ".vex", shell=True)
			elif platform.system() == "Darwin":
				retcode = subprocess.call("open " + fn + ".vex", shell=True)
			elif platform.system() == "Linux":
				print("Linux systems are not supported by Vex Coding Studio")
				exit()
			else:
				print("Unknown OS: '%s'" % platform.system())
				exit()
				
			if retcode < 0:
				print("Child was terminated by signal")
			else:
				pass
				#print("Child returned something idk")
		except:
			raise
			

elif __name__ == "__main__":
	print("Please specify parameters. Use the --help option for help.")
