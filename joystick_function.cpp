int joysticksensitivityfunction(int joystick)
{
	Int newvalue = 0;
	Int maxrange = 100;
	Int motormaxspeed = 127;

// formula
	Newvalue = ( joystickvalue ^ 3 ) / ( maxrange ^ 3 ) * ( motormaxspeed );
	Return(nawvalue);
}
