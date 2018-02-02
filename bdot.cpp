#include <iostream>
#include <Eigen/Geometry>
// using Eigen, a c++ library for linear algebra
using namespace Eigen;

/*
* function returns the desired magnetorquer output as a triaxial vector double
* arg 1: b, magnetic field strength: three-dimensional vector double
* arg 2: w (omega), angular velocity: three-dimensional vector double
* arg 3: k, positive gain: scalar double
* output: vector double of the form <x, y, z>
* Note: see 'Comparison of control laws for magnetic detumbling' equation (5)
*/
Vector3d magnetorquer_out(Vector3d mag_field_str, Vector3d ang_vel, double gain)
{
  // calculating scalar coefficient, -k / ||b||^2
  double scalar_coef = -gain / mag_field_str.dot(mag_field_str);
  // calculating m, magnetic dipole vector for the three magnetorquer coils
  Vector3d magnetic_dipoles = scalar_coef * (mag_field_str.cross(ang_vel));
  // returning torque, T, where T = m x b
  return magnetic_dipoles.cross(mag_field_str);
}
/*
* ***TEST***
* testing functionality using:
*   magnetic field strength = vector u = <1.0, 2.0, 3.0>
*   angular velocity = vector v = <5.0, 2.0, 5.0>
*   gain = 1.0
* expected output: [-23/7, 10/7, 1/7]
*/
int main()
{
  Vector3d u(1.0, 2.0, 3.0);
  Vector3d v(5.0, 2.0, 5.0);
  std::cout << magnetorquer_out(u, v, 1.0);
  return 0;
}
