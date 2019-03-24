
int joystickSensitivityFunction(int joystickValue)
{
  // Function to use a cubic function to smooth the power delivered to the motors 
  // This allows for more accurate turns and then full power if/when required.
  
  int newValue = 0;
  const int maxRange = 100;
  const int MaxPower = 127;
  
  // Cubic function that scales the output of the joystick to match maxPower of the motor desired  
  newValue = ( joystickValue ^ 3 ) / ( maxRange ^ 3 ) * maxPower;
  
  return(newValue);
}
