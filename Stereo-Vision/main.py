# Import local libraries
import vision

v = vision.Stereo()

v.B = 120           # mm
v.f = 6             # mm
v.f_pixels = 800    # px
v.s_h = 8.1         # mm
v.s_v = 7.2         # mm
v.p_s = 7.5         # um / px
v.h_max = 1080      # px
v.v_max = 960       # px
v.sp = 1/8          # px
v.m = 0.1           # px
v.p = 0.25          # px

# 1. Find minimum distance Zm
z_min = v.z_min()
print("Z_min:", round(z_min * 100, 2), "cm")

# 2. Find the disparity for an object located at a range Z = 1.2m
m = v.disparity(1.2)
print()
print("Disparity m at Z=1.2m:", round(m, 2), "px")

# 3. Plot the disparity d vs range Z for Z_min ≤ Z ≤ 5m.
v.disparity_vs_range(z_min, 5)

# 4. Find the range resolution r(Z) at Z = 1.2m.
r = v.range_resolution(1.2 * 1000)
print()
print("Range resolution at Z=1.2m:", round(r, 4), "mm")

# 5. Plot the range resolution r(Z) vs range Z for Z_min ≤ Z ≤ 5m
v.range_res_vs_range(z_min, 5)

# 6.  Compute ∆X, ∆Y and ∆Z at Z = 1.2m
dx, dy, dz = v.compute_deltas(1.2)
print()
print("∆X, ∆Y and ∆Z at Z = 1.2m")
print("Delta X:", round(dx*1000, 4),
      "mm\nDelta Y:", round(dy*1000, 4),
      "mm\nDelta Z:", round(dz*1000, 4), "mm")

# 7. Plot ∆X, ∆Y and ∆Z vs range Z for Z_min ≤ Z ≤ 5m
v.plot_deltas(z_min, 5)

# 8. Assume that the minimum disparity value that the stereo camera can measure is 1px.
# What would be the maximum range at which the stereo camera could provide a measurable
# distance?
z_max = v.max_range_measurable(1)
print("Max range distance:", z_max, "m")
