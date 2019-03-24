int joystickSensitivityFunction(int joystickValue)
{
  int newValue = 0;
  int maxRange = 100;
  int motorPower = 127;
  
  newValue = ( joystick ^ 3 ) / ( maxRange ^ 3 ) * motorPower;
  return(newValue);
}
