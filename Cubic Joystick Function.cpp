while(true) {
    
    int joystickSensitivityValue(int joystickValue){
        
        // This function outputs a low speed for low joystick value and high speed for high joystick value
        // This is cubic function instead of a linear function
        
        int newValue = 0;
        int maxRange = 100;
        int motorPowerPercentage = 100;
        
        newValue = (joystickValue ^ 3) / (maxRange ^ 3) * motorPowerPercentage;
            
        return(newValue)
    }
    // change direction of robots "front" and "back" to simplify driver's task
        if(Controller1.ButtonUp.pressing()) {   
            driveReverseDirection= true;
        }  
        if(Controller1.ButtonDown.pressing()) {              
            driveReverseDirection= false;
        }  
        if(!driveReverseDirection) {
            Leftfront.spin(vex::directionType::fwd, joystickSensitivityValue(Controller1.Axis3.value()), vex::velocityUnits::pct); //(Axis3+Axis4)/2
            Leftback.spin(vex::directionType::fwd, joystickSensitivityValue(Controller1.Axis3.value()), vex::velocityUnits::pct); //(Axis3+Axis4)/2
            Rightfront.spin(vex::directionType::fwd, joystickSensitivityValue(Controller1.Axis2.value()), vex::velocityUnits::pct);//(Axis3-Axis4)/2
            Rightback.spin(vex::directionType::fwd, joystickSensitivityValue(Controller1.Axis2.value()), vex::velocityUnits::pct);//(Axis3-Axis4)/2
        } else {
            // controls will be switched so now left is right side and vice versa.
            // motors spin opposite direction.
            // control sticks are swapped
            Leftfront.spin(vex::directionType::rev, joystickSensitivityValue(Controller1.Axis3.value()), vex::velocityUnits::pct); //(Axis3+Axis4)/2
            Leftback.spin(vex::directionType::rev, joystickSensitivityValue(Controller1.Axis3.value()), vex::velocityUnits::pct); //(Axis3+Axis4)/2
            Rightfront.spin(vex::directionType::rev, joystickSensitivityValue(Controller1.Axis2.value()), vex::velocityUnits::pct);//(Axis3-Axis4)/2
            Rightback.spin(vex::directionType::rev, joystickSensitivityValue(Controller1.Axis2.value()), vex::velocityUnits::pct);//(Axis3-Axis4)/2
      
        }
        if(Controller1.ButtonR1.pressing()){
            
    Leftpuncher.spin(directionType::fwd,100,velocityUnits::pct);
    Rightpuncher.spin(directionType::rev,100,velocityUnits::pct);
        }
        else{
            
    Leftpuncher.stop(brakeType::coast);
    Rightpuncher.stop(brakeType::coast);
        }
        }
        }
        