# Bismillah.

# Computer Graphics — slide-complete viva recall guide

**Primary sources read page by page**

- `Graphics/409/ARK_merged.pdf` — 473 physical PDF pages.
- `Graphics/409/IJ_merged2.pdf` — 263 physical PDF pages.
- Total audited coverage: **473 + 263 = 736 pages**. The exact, non-overlapping page-range matrix is at the end.

This is a reconstruction of concepts, not a list of memorized one-line answers. Equations are rewritten cleanly because several PDF text layers lose mathematical symbols. Source tags such as **[ARK 33–93]** and **[IJ 38–72]** refer to physical PDF pages.

## How to use this before a viva

For each topic, rehearse four layers:

1. **Definition:** one precise sentence.
2. **Mechanism:** what goes in, what happens, and what comes out.
3. **Equation or invariant:** the fact that makes the method correct.
4. **Example and limitation:** one whiteboard example plus one edge case.

When a panel says “explain,” begin with intuition, draw the smallest useful diagram, then write the equation. Do not begin by dumping an equation whose symbols you have not defined.

## The entire subject in one mental model

Computer graphics uses computers to **synthesize visual information**. A scene contains geometry, a camera, materials, and lights. A renderer answers: “What color should every displayed sample have?” **[IJ 1–36]**

Two major answers are:

- **Rasterization:** project primitives toward the screen, determine which pixel samples they cover, shade fragments, resolve visibility, and write a framebuffer. It is highly parallel and designed for real time.
- **Ray tracing:** launch a ray through each pixel, find its nearest scene intersection, then evaluate light transport using shadow, reflection, refraction, or randomly sampled path rays. It is naturally realistic but expensive.

The raster pipeline can be recalled as:

```text
model vertices
  -> model transform -> world coordinates
  -> view transform  -> camera/eye coordinates
  -> projection      -> homogeneous clip coordinates
  -> clipping
  -> perspective divide -> normalized device coordinates (NDC)
  -> viewport transform -> screen coordinates
  -> rasterization -> fragments
  -> fragment shading
  -> scissor/stencil/depth/blending
  -> color/depth/stencil framebuffer
```

The course’s motivating applications include animation, games, films, art and design, industrial design, computer-aided engineering, architecture, simulation, CAD, scientific visualization, UI, and research. Ivan Sutherland’s 1963 **Sketchpad**, created as his MIT PhD work on an oscilloscope-based system, pioneered interactive computer-aided design. The slides also use graphics’ Turing Awards to show the field’s importance: Sutherland received the 1988 award for foundational graphics work, while Edwin Catmull and Pat Hanrahan shared the 2019 award for fundamental 3D-graphics contributions and their impact on computer-generated imagery. Major research venues named in the slides include ACM SIGGRAPH, SIGGRAPH Asia, and Eurographics. **[IJ 2–21]**

---

# Part I — mathematical language of graphics

## 1. Points, vectors, and coordinate frames **[IJ 38–54]**

### Point versus vector

- A **point** describes a location.
- A **vector** describes a magnitude and direction; it may represent displacement, velocity, a surface normal, or a coordinate-axis direction.
- Point minus point is a vector: `v = Q - P`.
- Point plus vector is a point: `Q = P + v`.
- Vector plus vector is a vector.

Coordinates only have meaning relative to a frame. The tuple `(1,2,3)` may describe a model-space point, a world-space point, or a direction in a camera frame. Always state the space.

### Basic operations

For `a=(a_x,a_y,a_z)` and `b=(b_x,b_y,b_z)`:

$$
a+b=(a_x+b_x,a_y+b_y,a_z+b_z),\qquad sa=(sa_x,sa_y,sa_z)
$$

$$
\lVert a\rVert=\sqrt{a_x^2+a_y^2+a_z^2},\qquad \hat a=\frac{a}{\lVert a\rVert}
$$

Normalization retains direction and changes length to one. It is undefined for the zero vector; code must test against an epsilon.

### Dot product

$$
a\cdot b=a_xb_x+a_yb_y+a_zb_z=\lVert a\rVert\lVert b\rVert\cos\theta
$$

Uses:

- Angle: `cos(theta) = dot(a,b)/(|a||b|)`; clamp the computed cosine to `[-1,1]` before `acos`.
- Orthogonality: nonzero vectors are perpendicular iff `a·b=0`.
- Front/back or illumination tests: the sign of `N·L`, `N·V`, or a plane equation.
- Projection onto a unit vector `v`: `proj_v(c)=(c·v)v`.
- Rejection: `c_perp = c - (c·v)v`.

Properties: symmetry, linearity, homogeneity, and `a·a=|a|²`.

### Perpendicular vector in 2D

For `a=(a_x,a_y)`, a counterclockwise perpendicular is

$$
a^\perp=(-a_y,a_x).
$$

Thus a 2D rotation can be understood geometrically as

$$
R_\theta a=a\cos\theta+a^\perp\sin\theta.
$$

### Cross product

$$
a\times b=
\begin{bmatrix}
a_yb_z-a_zb_y\\
a_zb_x-a_xb_z\\
a_xb_y-a_yb_x
\end{bmatrix}
$$

It is perpendicular to both operands, follows the right-hand rule, and has magnitude

$$
\lVert a\times b\rVert=\lVert a\rVert\lVert b\rVert\sin\theta,
$$

which is the parallelogram area. Triangle area is half of that. It is anti-commutative: `a×b=-(b×a)`; therefore operand order controls normal orientation.

For a triangle `(A,B,C)` with counterclockwise winding,

$$
N=\operatorname{normalize}((B-A)\times(C-A)).
$$

### Scalar triple product

$$
a\cdot(b\times c)
$$

is the signed parallelepiped volume. It is zero exactly when the three vectors are coplanar (up to numerical tolerance). This gives a useful line-line coplanarity test.

### Reflection of a vector

If incident direction `I` points **toward** the surface and `N` is a unit normal,

$$
R=I-2(I\cdot N)N.
$$

If instead `L` points from the surface **toward the light**, the reflected light direction is

$$
R=2(N\cdot L)N-L.
$$

These are the same geometry with opposite input-direction conventions—a common viva trap.

**Viva line:** “A dot product measures alignment; a cross product produces an oriented perpendicular and area.”

## 2. Lines, rays, and planes **[IJ 55–70; ARK 33–39]**

### Line and ray

Through point `P0` with nonzero direction `d`:

$$
P(t)=P_0+td.
$$

- Infinite line: `t` is any real number.
- Ray: `t>=0`, normally `t>=epsilon` in rendering.
- Segment from `A` to `B`: `P(t)=(1-t)A+tB`, `0<=t<=1`.

If `d` is normalized, `t` is physical distance; otherwise it is only a parameter.

### Four plane representations

1. **Three points:** non-collinear `A,B,C`; normal `(B-A)×(C-A)`.
2. **Parametric:** `P(s,t)=P0+s a+t b`, where `a,b` are independent in-plane directions.
3. **Point-normal:** `n·(P-P0)=0`.
4. **Implicit:** `Ax+By+Cz+D=0`, where `n=(A,B,C)` and `D=-n·P0`.

If `n` is unit length, signed point-plane distance is

$$
d(P)=n\cdot(P-P_0)=n\cdot P+D.
$$

For a non-unit normal, divide by `|n|`. The sign identifies the chosen front and back half-spaces.

### Ray-plane intersection: derivation

Substitute `P(t)=O+td` into `n·P+D=0`:

$$
n\cdot O+t(n\cdot d)+D=0
$$

$$
\boxed{t=-\frac{n\cdot O+D}{n\cdot d}}
$$

Then `H=O+td`.

Cases:

- `|n·d|<epsilon` and `|n·O+D|<epsilon`: ray lies in the plane; infinitely many mathematical intersections.
- `|n·d|<epsilon` otherwise: parallel, no intersection.
- `t<t_min`: intersection is behind the usable ray origin or too close.
- Track the smallest valid `t<t_current` to retain the nearest hit.

For a normalized normal, `n·d<0` means the ray approaches the normal-facing side under the usual convention.

```cpp
bool hitPlane(Vec3 O, Vec3 d, Vec3 n, double D,
              double tMin, double tMax, double& t) {
    double denom = dot(n, d);
    if (std::abs(denom) < 1e-9) return false;
    double candidate = -(dot(n, O) + D) / denom;
    if (candidate < tMin || candidate > tMax) return false;
    t = candidate;
    return true;
}
```

Time is `O(1)` and extra space is `O(1)`.

**Worked line-plane example:** let the plane be

$$
x+2y+3z+4=0
$$

and the line be

$$
P(t)=(1,2,3)+t(3,2,1).
$$

Substitution gives

$$
(1+3t)+2(2+2t)+3(3+t)+4=18+10t=0,
$$

so `t=-1.8` and the intersection is

$$
P(-1.8)=(-4.4,-1.6,1.2).
$$

Checking in the plane equation gives `-4.4-3.2+3.6+4=0`. The negative parameter is important: the **infinite line** intersects, but a ray starting at `(1,2,3)` and pointing along `(3,2,1)` does not hit the plane in its forward direction.

### Line-line relations in 3D

For `L1=P1+tV1` and `L2=P2+sV2`:

- Parallel when `|V1×V2|≈0`.
- If parallel and `|(P2-P1)×V1|≈0`, they are coincident.
- If not parallel, the lines can intersect only if

$$
(P_2-P_1)\cdot(V_1\times V_2)=0.
$$

That scalar-triple-product condition says both lines are coplanar. In floating-point work it is tested with a scaled tolerance. To find the intersection, solve two component equations for `t,s`, then verify all three components. Nonparallel, noncoplanar 3D lines are **skew**.

**Worked slide exercise:**

$$
L_1=(1,2,3)+t(1,1,1),\quad L_2=(1,1,1)+s(1,2,3).
$$

Equating x gives `t=s`. Equating y gives `2+t=1+2t`, so `t=s=1`. z verifies `3+1=1+3`; intersection is `(2,3,4)`.

### Plane-plane intersection

Write planes as `n1·x=d1` and `n2·x=d2`.

- If `n1×n2=0`, they are parallel; they are either distinct or coincident.
- Otherwise their intersection is a line with direction

$$
u=n_1\times n_2.
$$

A point on the line is

$$
p_0=\frac{(d_1n_2-d_2n_1)\times u}{\lVert u\rVert^2}.
$$

Then `p(t)=p0+t u`. An alternative slide method sets one coordinate, such as `z=0`, and solves the resulting three equations; if that auxiliary plane is parallel to the intersection line, choose another coordinate.

## 3. Barycentric coordinates **[ARK 40–60; ARK 439–443]**

For nondegenerate triangle `(A,B,C)`, every point in its plane has

$$
P=\alpha A+\beta B+\gamma C,\qquad \alpha+\beta+\gamma=1.
$$

Equivalently,

$$
P=A+\beta(B-A)+\gamma(C-A),\qquad \alpha=1-\beta-\gamma.
$$

The edge vectors `(B-A)` and `(C-A)` form a basis for the triangle’s plane. The weights also equal signed opposite-subtriangle area ratios:

$$
\alpha=\frac{[PBC]}{[ABC]},\quad
\beta =\frac{[PCA]}{[ABC]},\quad
\gamma=\frac{[PAB]}{[ABC]}.
$$

Inside/boundary test:

$$
\alpha,\beta,\gamma\ge 0
$$

with epsilon-aware comparisons. In the two-coordinate form, test `beta>=0`, `gamma>=0`, and `beta+gamma<=1`.

Any per-vertex attribute can be interpolated:

$$
a(P)=\alpha a_A+\beta a_B+\gamma a_C.
$$

Uses include colors, normals, depth, UV coordinates, and world position. Normalize an interpolated normal before lighting.

For perspective-correct attributes after projection, ordinary screen-space interpolation is wrong. If clip-space `w_i` are known:

$$
a(P)=\frac{\alpha a_A/w_A+\beta a_B/w_B+\gamma a_C/w_C}
{\alpha/w_A+\beta/w_B+\gamma/w_C}.
$$

**Invariant:** the weights sum to one, so affine transformations commute with barycentric interpolation.

---

# Part II — transformations and coordinate spaces

## 4. Transformation families **[IJ 73–84]**

A geometric transformation maps a point `p` to `p'`. It is used for modeling, animation, deformation, camera viewing, projection, and shadow construction.

| Family | General behavior | What it preserves | Examples |
|---|---|---|---|
| Euclidean/rigid | rotation + translation, possibly reflection if orientation reversal is allowed | distances and angles | translate, rotate |
| Similarity | rigid transform + uniform scale | angles and length ratios | isotropic scaling |
| Linear | `p'=Ap`; origin stays fixed | straight lines and linear combinations | nonuniform scale, rotation, reflection, shear |
| Affine | `p'=Ap+t` | lines, parallelism, ratios along a line | every linear transform + translation |
| Projective | homogeneous linear map followed by division | collinearity; cross-ratio | perspective projection |

Viva traps:

- Translation is affine but not linear in ordinary Cartesian coordinates because it does not map the origin to itself.
- Perspective preserves straight lines but generally not parallelism, length, or angle.
- Scaling by zero is not invertible.

## 5. Homogeneous coordinates **[IJ 85–92]**

Homogeneous coordinates add one component so translation becomes matrix multiplication.

- 2D point `(x,y)` becomes `(x,y,1)^T`; use `3x3` matrices.
- 3D point `(x,y,z)` becomes `(x,y,z,1)^T`; use `4x4` matrices.
- A direction has `w=0`; translation therefore does not affect it.
- Equivalent homogeneous points differ by a nonzero scale: `(x,y,w) ~ (kx,ky,kw)`.
- Convert back by division: `(x,y,w) -> (x/w,y/w)` when `w!=0`.
- `w=0` represents a point/direction at infinity, central to projective geometry and vanishing points.

An affine 3D matrix for column vectors is

$$
M=\begin{bmatrix}
 & & &t_x\\
 &A& &t_y\\
 & & &t_z\\
0&0&0&1
\end{bmatrix}.
$$

## 6. Basic 2D and 3D matrices **[IJ 93–107]**

This guide uses **column vectors**, so `p'=Mp`.

### Translation

$$
T(t_x,t_y,t_z)=
\begin{bmatrix}
1&0&0&t_x\\0&1&0&t_y\\0&0&1&t_z\\0&0&0&1
\end{bmatrix}.
$$

Inverse: `T(t)^-1=T(-t)`.

### Scaling

$$
S(s_x,s_y,s_z)=
\begin{bmatrix}
s_x&0&0&0\\0&s_y&0&0\\0&0&s_z&0\\0&0&0&1
\end{bmatrix}.
$$

Uniform scaling has equal factors. Differential/nonuniform scaling does not preserve general angles. The inverse exists only when every scale factor is nonzero.

### Rotation in 2D / about z

$$
R_z(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0&0\\
\sin\theta& \cos\theta&0&0\\
0&0&1&0\\0&0&0&1
\end{bmatrix}.
$$

### Rotations about x and y

$$
R_x(\theta)=
\begin{bmatrix}
1&0&0&0\\
0&c&-s&0\\
0&s&c&0\\
0&0&0&1
\end{bmatrix},\qquad
R_y(\theta)=
\begin{bmatrix}
c&0&s&0\\
0&1&0&0\\
-s&0&c&0\\
0&0&0&1
\end{bmatrix}.
$$

Here `c=cos(theta)`, `s=sin(theta)` and positive direction follows the right-hand rule.

### Reflection

In 2D homogeneous form:

$$
M_x=\operatorname{diag}(1,-1,1),\qquad
M_y=\operatorname{diag}(-1,1,1).
$$

A reflection reverses orientation; its determinant is negative. Applying the same axis reflection twice gives identity, so `M^-1=M`.

### Shear

For 2D:

$$
H_x(k)=\begin{bmatrix}1&k&0\\0&1&0\\0&0&1\end{bmatrix},\quad x'=x+ky,
$$

$$
H_y(k)=\begin{bmatrix}1&0&0\\k&1&0\\0&0&1\end{bmatrix},\quad y'=kx+y.
$$

In 3D, a z-dependent xy shear can use `x'=x+k_xz`, `y'=y+k_yz`, `z'=z`.

### Rotation matrices: essential properties

For a pure rotation `R`:

$$
R^TR=I,\qquad R^{-1}=R^T,\qquad \det R=+1.
$$

Rows and columns are mutually perpendicular unit vectors. A reflection is also orthogonal but has determinant `-1`.

## 7. Composition and matrix order **[IJ 108–118; ARK 409–416]**

With column vectors, the **rightmost transform happens first**:

$$
p'=CBAp
$$

means apply `A`, then `B`, then `C`. Matrix multiplication is associative but generally not commutative.

### Exact slide example: scale and translate

Start with `p=(1,1,1)^T`, scale by `(2,2)`, then translate by `(3,1)`:

$$
p'=T(3,1)S(2,2)p=(5,3,1)^T.
$$

The composite is

$$
TS=
\begin{bmatrix}1&0&3\\0&1&1\\0&0&1\end{bmatrix}
\begin{bmatrix}2&0&0\\0&2&0\\0&0&1\end{bmatrix}
=
\begin{bmatrix}2&0&3\\0&2&1\\0&0&1\end{bmatrix}.
$$

Reverse the order:

$$
ST=
\begin{bmatrix}2&0&6\\0&2&2\\0&0&1\end{bmatrix},
$$

so `STp=(8,4,1)^T`. Translation itself gets scaled in the second case.

### Rotate about a pivot

To rotate by `theta` about `P=(h,k)`:

$$
M=T(h,k)R(\theta)T(-h,-k).
$$

Whiteboard example: rotate `Q=(3,2)` by 90 degrees counterclockwise about `P=(1,1)`.

```text
Q-P = (2,1)
rotate 90° -> (-1,2)
add P -> (0,3)
```

### Reflect about an arbitrary 2D line

For a line through `(0,b)` making angle `theta` with the x-axis:

$$
M=T(0,b)R(\theta)M_xR(-\theta)T(0,-b).
$$

The logic is always: move the special geometry to a canonical position, perform the easy canonical transform, then undo the alignment.

### Efficiency of composition

For one point, applying nested matrices can be fine. For many vertices, first compute `M=CBA`, then use `Mp` for every vertex. This is exactly why a model matrix is prepared once per object/draw call.

### Model matrix convention

A common local-to-world model matrix is

$$
M=T\,R\,S.
$$

It applies local scale, then rotation, then world translation. It is a convention, not an immutable law; understand the desired geometric order.

## 8. Arbitrary-axis rotation and Rodrigues’ formula **[IJ 119–136]**

Let `k=(k_x,k_y,k_z)` be a **unit** rotation axis and `v` the vector to rotate by angle `theta`. Decompose `v` into an axis-parallel part and a perpendicular part. The coordinate-free result is

$$
\boxed{R_k(\theta)v=
v\cos\theta+(k\times v)\sin\theta+k(k\cdot v)(1-\cos\theta)}.
$$

Matrix form:

$$
R=\cos\theta I+(1-\cos\theta)kk^T+\sin\theta[k]_\times,
$$

where

$$
[k]_\times=
\begin{bmatrix}
0&-k_z&k_y\\k_z&0&-k_x\\-k_y&k_x&0
\end{bmatrix}
$$

and `[k]_x v=k×v`.

Expanded:

$$
R=\begin{bmatrix}
c+k_x^2(1-c)&k_xk_y(1-c)-k_zs&k_xk_z(1-c)+k_ys\\
k_yk_x(1-c)+k_zs&c+k_y^2(1-c)&k_yk_z(1-c)-k_xs\\
k_zk_x(1-c)-k_ys&k_zk_y(1-c)+k_xs&c+k_z^2(1-c)
\end{bmatrix}.
$$

To rotate around an axis passing through point `q`, use

$$
T(q)R_k(\theta)T(-q).
$$

The slides also construct arbitrary-axis rotation by aligning the axis with z, applying `R_z(theta)`, then undoing alignment. If `A` maps `k` to z, the result is `A^T R_z(theta) A`. Rodrigues gives the same result without manually managing five rotations.

### Recover axis-angle from a rotation matrix

For a proper rotation away from the singular cases:

$$
\theta=\cos^{-1}\left(\frac{\operatorname{tr}(R)-1}{2}\right),
$$

$$
k=\frac{1}{2\sin\theta}
\begin{bmatrix}
R_{32}-R_{23}\\R_{13}-R_{31}\\R_{21}-R_{12}
\end{bmatrix}.
$$

Edge cases:

- Near `theta=0`, the axis is poorly determined; use a small-angle method.
- Near `theta=pi`, `sin(theta)` is near zero; derive the axis from diagonal terms/eigenvector instead.
- Clamp `(trace(R)-1)/2` to `[-1,1]` before `acos`.

## 9. Correct transformation of normals

If points transform by `p'=Mp`, a normal generally does **not** transform by `M`. To remain perpendicular to transformed tangents:

$$
n'\propto(M^{-1})^Tn.
$$

Use the upper-left `3x3` linear part, then normalize. For rotation or uniform scale, simpler transformations happen to work; nonuniform scaling exposes the error.

GLSL:

```glsl
mat3 normalMatrix = transpose(inverse(mat3(model)));
vec3 worldNormal = normalize(normalMatrix * aNormal);
```

**Viva trap:** `w=0` prevents translation of a direction, but that alone does not correctly handle a normal under nonuniform scale.

---

# Part III — camera, viewing, and projection

## 10. Camera models **[ARK 94–130; IJ 138–198]**

### Physical pinhole camera

A pinhole admits one ray per ideal image point, producing an inverted image on a plane behind the hole. It has perfect geometric focus but very low light throughput. If `H` is the hole and `X` is a sensor point behind it:

$$
O=H,\qquad d=\operatorname{normalize}(H-X).
$$

Graphics usually moves a **virtual image plane** in front of the eye. This is physically unrealizable but produces an upright construction:

$$
O=eye,\qquad d=\operatorname{normalize}(pixel-eye).
$$

### Perspective camera

All primary rays share the camera origin but pass through different image-plane samples. Distant objects subtend smaller angles and therefore look smaller. This gives foreshortening, convergence of projected parallel lines, and depth perception.

### Orthographic camera

All primary rays have the same direction and different origins on the image plane:

$$
O_{ij}=pixel_{ij},\qquad d=forward.
$$

There is no perspective foreshortening: apparent size is independent of depth. Uses include CAD, engineering drawings, architectural views, 2D games, and precise measurement.

| Property | Perspective | Orthographic |
|---|---|---|
| Ray geometry | common origin, divergent | parallel |
| Size with depth | decreases with distance | constant |
| Parallel lines | may converge | stay parallel |
| Typical use | realistic scenes | CAD/measurement |

## 11. Camera basis and primary-ray generation **[ARK 111–130]**

Let camera position be `e`, with orthonormal directions `u` (right), `v` (up), and `w` (forward toward the image plane in the ARK slide convention). Let image distance be `d`, horizontal field of view `fov_x`, resolution `W x H`, and aspect `W/H`.

Image-plane half-width and half-height are

$$
X=d\tan(fov_x/2),\qquad Y=X\frac{H}{W}.
$$

For pixel `(i,j)`, sample its center, map to `[-1,1]^2`, then scale:

$$
s=\left(2\frac{i+0.5}{W}-1\right)X,
$$

$$
t=\left(2\frac{j+0.5}{H}-1\right)Y.
$$

The world-space sample is

$$
pixel=e+dw+su+tv.
$$

Then a perspective ray is `normalize(pixel-e)`. If image rows increase downward, negate the t expression or reverse the up vector. If the supplied FOV is vertical instead, first compute `Y=d tan(fov_y/2)` and set `X=Y(W/H)`.

```cpp
Ray makePerspectiveRay(int i, int j, int W, int H,
                       Vec3 eye, Vec3 right, Vec3 up, Vec3 forward,
                       double horizontalFovRadians, double imageDistance) {
    double halfW = imageDistance * std::tan(horizontalFovRadians * 0.5);
    double halfH = halfW * static_cast<double>(H) / W;
    double s = (2.0 * (i + 0.5) / W - 1.0) * halfW;
    double t = (1.0 - 2.0 * (j + 0.5) / H) * halfH; // row 0 is top
    Vec3 pixel = eye + imageDistance * forward + s * right + t * up;
    return {eye, normalize(pixel - eye)};
}
```

**Worked center-pixel check:** for an odd resolution, the center sample gives `s=t=0`; its ray must equal the forward direction. This is a powerful debugging invariant.

## 12. Constructing the view/LookAt transform **[IJ 169–188]**

The view transform changes coordinates; it does not physically move the world. Its goal is to represent the scene in a canonical camera frame where the eye is at the origin and, in OpenGL convention, looks along negative z.

Given `eye`, `target`, and a nonparallel approximate `up0`:

$$
f=\operatorname{normalize}(target-eye),
$$

$$
r=\operatorname{normalize}(f\times up_0),
$$

$$
u=r\times f.
$$

For column vectors, a standard right-handed OpenGL-style view matrix is

$$
V=\begin{bmatrix}
r_x&r_y&r_z&-r\cdot eye\\
u_x&u_y&u_z&-u\cdot eye\\
-f_x&-f_y&-f_z& f\cdot eye\\
0&0&0&1
\end{bmatrix}.
$$

Why the dot products? A world point `p` is first translated to `p-eye`; each camera coordinate is its projection onto a camera axis. The matrix combines that translation and rotation.

Checks:

- `V * [eye,1]^T = [0,0,0,1]^T`.
- `r,u,-f` are mutually orthogonal unit vectors.
- A point directly in front has negative camera-space z in this convention.

Degenerate case: if `up0` is parallel or nearly parallel to `f`, `f×up0` vanishes. Choose a fallback up vector.

Legacy OpenGL from the slides:

```cpp
glViewport(0, 0, windowWidth, windowHeight);

glMatrixMode(GL_PROJECTION);
glLoadIdentity();
gluPerspective(60.0, aspect, 1.0, 1000.0);

glMatrixMode(GL_MODELVIEW);
glLoadIdentity();
gluLookAt(3, 3, 2,   0, 0, 0,   0, 0, 1);
glRotatef(theta, 0, 0, 1);
glScalef(zoom, zoom, zoom);
```

This teaches matrix roles, although modern OpenGL calculates matrices in the application and passes them as shader uniforms.

## 13. Projection taxonomy **[IJ 138–168; IJ 189–198]**

A projection maps an n-dimensional representation to a lower-dimensional one. Here, straight projectors map 3D points to a 2D plane.

### Central/perspective versus parallel

- Finite center of projection (COP) -> perspective.
- COP at infinity -> parallel projectors.

Parallel projection divides into:

- **Orthographic:** direction of projection (DOP) is normal to the projection plane.
- **Oblique:** DOP is not normal to the plane.

Orthographic includes front/top/side views and axonometric views. In **isometric** projection, the projection-plane normal makes equal absolute angles with all three principal axes, so `|d_x|=|d_y|=|d_z|`. Axonometric foreshortening is uniform by direction, unlike distance-dependent perspective foreshortening.

Oblique forms:

- **Cavalier:** receding-axis scale `lambda=1`, typically `alpha=45°`; full depth retained.
- **Cabinet:** `lambda=1/2`, `alpha≈63.4°`; depth is halved and usually looks less distorted.
- Orthographic is the limiting `lambda=0`, `alpha=90°` case.

With receding direction angle `beta` in the view plane:

$$
x'=x+\lambda z\cos\beta,\qquad
y'=y+\lambda z\sin\beta.
$$

The corresponding row pair is `[1,0,lambda cos beta]` and `[0,1,lambda sin beta]`. Sign depends on the chosen z/DOP convention.

### Vanishing points

Under perspective projection, a family of parallel 3D lines not parallel to the view plane appears to converge at a vanishing point. Principal vanishing points correspond to principal axes cut by the projection plane:

- one-point perspective: one principal direction converges;
- two-point: two converge;
- three-point: all three converge.

There are infinitely many possible vanishing points—one per eligible line direction—but at most three principal-axis vanishing points.

## 14. Perspective projection derivation **[IJ 157–168]**

Put the COP at the origin and projection plane at `z=d`. For `P=(x,y,z)`, similar triangles give

$$
\frac{x'}d=\frac{x}z,\qquad \frac{y'}d=\frac{y}z.
$$

Hence

$$
\boxed{x'=\frac{dx}{z},\qquad y'=\frac{dy}{z},\qquad z'=d.}
$$

**Worked example:** `P=(4,2,8)` and `d=2` project to `(1,0.5,2)`. Doubling all of `x,y,z` leaves the 2D projection unchanged; points along one projector map to one image point.

A homogeneous matrix producing `(dx,dy,dz,z)` before division is

$$
P_d=\begin{bmatrix}
d&0&0&0\\0&d&0&0\\0&0&d&0\\0&0&1&0
\end{bmatrix}.
$$

Dividing by `w=z` yields the desired coordinates. This cleanly illustrates why perspective requires homogeneous division and is not an affine transformation.

### Projection onto a general plane from the origin

Let the plane contain `R0` and have normal `n`; write

$$
n\cdot X=d_0,\qquad d_0=n\cdot R_0.
$$

The projector from the origin through `P` is `X=lambda P`. Enforce the plane equation:

$$
\lambda=\frac{d_0}{n\cdot P},\qquad
P'=\frac{d_0P}{n\cdot P}.
$$

Homogeneous output `(d0 x,d0 y,d0 z,n·P)` is produced by

$$
M=\begin{bmatrix}
d_0&0&0&0\\0&d_0&0&0\\0&0&d_0&0\\n_x&n_y&n_z&0
\end{bmatrix}.
$$

If `n·P=0`, the projector is parallel to the plane and the projected point is at infinity.

For arbitrary COP `C`, parameterize the projector as `C+t(P-C)`:

$$
t=\frac{n\cdot(R_0-C)}{n\cdot(P-C)},\qquad
P'=C+t(P-C).
$$

This is equivalent to translating `C` to the origin, applying the origin-COP projection, then translating back.

## 15. Standard perspective and orthographic matrices **[ARK 410–415]**

For a symmetric right-handed OpenGL perspective frustum with vertical FOV `fovy`, aspect `a`, near `n>0`, far `f>n`, camera looking down `-z`:

$$
P=\begin{bmatrix}
\frac{1}{a\tan(fovy/2)}&0&0&0\\
0&\frac{1}{\tan(fovy/2)}&0&0\\
0&0&-\frac{f+n}{f-n}&-\frac{2fn}{f-n}\\
0&0&-1&0
\end{bmatrix}.
$$

For orthographic bounds `[l,r] x [b,t]` and positive near/far distances under the same convention:

$$
O=\begin{bmatrix}
\frac2{r-l}&0&0&-\frac{r+l}{r-l}\\
0&\frac2{t-b}&0&-\frac{t+b}{t-b}\\
0&0&-\frac2{f-n}&-\frac{f+n}{f-n}\\
0&0&0&1
\end{bmatrix}.
$$

Projection conventions vary. Traditional OpenGL NDC z is `[-1,1]`; Direct3D/Vulkan commonly use `[0,1]` (with further coordinate/orientation differences). State the convention before comparing matrices.

## 16. Clip space, NDC, and viewport **[ARK 413–415; ARK 430–435]**

The vertex shader outputs homogeneous clip coordinate `c=(x_c,y_c,z_c,w_c)`. In the symmetric OpenGL slide convention it is inside when

$$
-w_c\le x_c,y_c,z_c\le w_c.
$$

Clipping happens **before** division. Then

$$
(x_n,y_n,z_n)=\left(\frac{x_c}{w_c},\frac{y_c}{w_c},\frac{z_c}{w_c}\right)
$$

lies in the canonical NDC cube. A viewport with origin `(x0,y0)`, width `W`, height `H` maps

$$
x_s=x_0+\frac{x_n+1}{2}W,\qquad
y_s=y_0+\frac{y_n+1}{2}H.
$$

If a windowing system places y=0 at the top, the y mapping is flipped.

**Why clip before divide?** Homogeneous plane tests remain linear and correctly handle primitives crossing the eye/near plane. Dividing first can create infinities and broken interpolation.

---

# Part IV — scan conversion and raster algorithms

The ARK deck emphasizes modern triangle rasterization **[ARK 437–444]**. The line, circle, fill, and classic clipping algorithms below are included as viva-critical scan-conversion material; they are not standalone chapters in the two merged decks.

## 17. Raster, pixel, sample, fragment

- A raster display is a finite grid of pixels.
- A **sample** is a location at which coverage/visibility/shading is evaluated; a pixel can contain one or many samples.
- A **fragment** is a candidate contribution generated by rasterization. It carries screen position, depth, interpolated attributes, and coverage.
- A fragment is not yet a final pixel: it may fail scissor, stencil, or depth tests, be discarded by a shader, or blend with an existing color.

Scan conversion converts continuous geometric primitives to discrete covered samples. Rounding, tie-breaking, and shared-edge rules matter because the output grid is discrete.

## 18. DDA line drawing

Given endpoints `(x0,y0)`, `(x1,y1)`:

$$
dx=x_1-x_0,\qquad dy=y_1-y_0,
$$

$$
steps=\max(|dx|,|dy|),\quad x_{inc}=dx/steps,\quad y_{inc}=dy/steps.
$$

Starting from `(x0,y0)`, plot the rounded coordinates and add the increments `steps` times.

```cpp
std::vector<std::pair<int,int>> ddaLine(double x0, double y0,
                                        double x1, double y1) {
    double dx = x1 - x0, dy = y1 - y0;
    int steps = static_cast<int>(std::max(std::abs(dx), std::abs(dy)));
    std::vector<std::pair<int,int>> out;
    if (steps == 0) {
        out.push_back({static_cast<int>(std::lround(x0)),
                       static_cast<int>(std::lround(y0))});
        return out;
    }
    double x = x0, y = y0;
    double xInc = dx / steps, yInc = dy / steps;
    for (int k = 0; k <= steps; ++k) {
        out.push_back({static_cast<int>(std::lround(x)),
                       static_cast<int>(std::lround(y))});
        x += xInc; y += yInc;
    }
    return out;
}
```

- Time: `O(max(|dx|,|dy|))`; output itself has that size.
- Strength: simple and handles every slope.
- Weakness: floating-point addition and rounding; accumulated error can drift.
- Edge case: coincident endpoints must not divide by zero.

**Whiteboard example:** `(2,2)` to `(7,5)` gives `dx=5`, `dy=3`, `steps=5`, increments `(1,0.6)`. Rounded samples: `(2,2),(3,3),(4,3),(5,4),(6,4),(7,5)`.

## 19. Bresenham line drawing

Bresenham chooses between neighboring pixels using an integer decision error. It avoids per-step floating-point multiplication/division.

### Derivation for `0<=slope<=1`

Implicit line function:

$$
F(x,y)=dy(x-x_0)-dx(y-y_0).
$$

At each x step, choose east `E=(x+1,y)` or northeast `NE=(x+1,y+1)` according to the sign at their midpoint. A scaled decision variable begins

$$
p_0=2dy-dx.
$$

- If `p<0`, choose E and update `p += 2dy`.
- Otherwise choose NE and update `p += 2(dy-dx)`.

### All-octant implementation

```cpp
std::vector<std::pair<int,int>> bresenhamLine(int x0, int y0,
                                              int x1, int y1) {
    std::vector<std::pair<int,int>> out;
    int dx = std::abs(x1 - x0), sx = (x0 < x1) ? 1 : -1;
    int dy = -std::abs(y1 - y0), sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy;
    while (true) {
        out.push_back({x0,y0});
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy; }
    }
    return out;
}
```

Invariant: after every iteration, `(x,y)` is the chosen raster position and `err` represents the signed discrepancy between ideal progress in x and y. The algorithm is symmetric under endpoint reversal, handles steep/negative/vertical lines, and runs in `O(max(|dx|,|dy|))` time with `O(1)` working space.

### DDA versus Bresenham

| Feature | DDA | Bresenham |
|---|---|---|
| Arithmetic | floating increments + rounding | integer addition/comparison |
| Error | may accumulate | bounded decision error |
| Simplicity | conceptually simplest | slightly more involved |
| Historical software rasterization | adequate | usually preferred |

Modern GPUs use highly parallel hardware edge equations, not a literal classroom Bresenham loop.

## 20. Midpoint/Bresenham circle

A circle centered at the origin satisfies

$$
F(x,y)=x^2+y^2-r^2=0.
$$

Compute only the first octant and use eight-way symmetry:

```text
(+x,+y), (-x,+y), (+x,-y), (-x,-y),
(+y,+x), (-y,+x), (+y,-x), (-y,-x)
```

Starting at `(0,r)`, decide between E `(x+1,y)` and SE `(x+1,y-1)` by evaluating the implicit function near the midpoint. An integer form uses `d=1-r`.

```cpp
void midpointCircle(int xc, int yc, int r,
                    const std::function<void(int,int)>& plot) {
    auto plot8 = [&](int x, int y) {
        plot(xc+x,yc+y); plot(xc-x,yc+y);
        plot(xc+x,yc-y); plot(xc-x,yc-y);
        plot(xc+y,yc+x); plot(xc-y,yc+x);
        plot(xc+y,yc-x); plot(xc-y,yc-x);
    };
    if (r < 0) return;
    int x = 0, y = r, d = 1 - r;
    plot8(x,y);
    while (x < y) {
        ++x;
        if (d < 0) {
            d += 2*x + 1;
        } else {
            --y;
            d += 2*(x-y) + 1;
        }
        plot8(x,y);
    }
}
```

Time is `O(r)` and working space is `O(1)`. For `r=0`, plot the center once; symmetry may otherwise write duplicate pixels, which is harmless unless writes are expensive.

### Midpoint ellipse recall

For `F(x,y)=r_y²x²+r_x²y²-r_x²r_y²`, begin at `(0,r_y)`. Region 1 advances x while the tangent magnitude satisfies `2r_y²x < 2r_x²y`; region 2 advances mainly y. Use four-way symmetry. The algorithm switches decision recurrences at the point where slope magnitude crosses one. In a viva, explain the two regions and implicit-function decision before attempting all recurrence constants.

## 21. Polygon scanline filling

For each horizontal scanline, polygon edges produce intersection x values. Sort them and fill between pairs under the even-odd rule.

Efficient implementation uses:

- **Edge Table (ET):** buckets nonhorizontal edges by their lower scanline; each record stores `y_max`, current `x`, and inverse slope `dx/dy`.
- **Active Edge Table (AET):** edges crossing the current scanline, sorted by x.

```text
build ET from every nonhorizontal edge
for y from lowest relevant row to highest:
    add ET[y] edges to AET
    remove edges whose y_max == y
    sort AET by current x (and a deterministic tie rule)
    fill pixels between intersection pairs
    for each active edge: x += dx/dy
```

Critical shared-vertex rule: treat edges as **lower-inclusive, upper-exclusive** (`y_min <= y < y_max`). Otherwise a local maximum/minimum can be counted twice and invert parity incorrectly. Ignore horizontal edges in the intersection list, though they still contribute to a drawn boundary.

Complexity for `H` scanlines, `E` edges, and `P` filled pixels is approximately `O(E log E + H*active-sort + P)`; with coherent insertion sorting, active-edge updates are usually cheap. Space is `O(E)`.

### Even-odd and nonzero winding rules

- Even-odd: crossing an edge toggles inside/outside.
- Nonzero winding: signed crossings accumulate; a point is inside when winding number is nonzero.

The winding rule handles nested contours with orientation-sensitive holes.

### Boundary fill versus flood fill

- **Boundary fill:** start inside and expand until a boundary color is reached.
- **Flood fill:** replace a connected region of a target color.
- 4-connected uses north/south/east/west; 8-connected also follows diagonals.

Recursive versions can overflow the call stack on large regions. Use an explicit stack/queue or scanline seed fill. Both can require `O(number of region pixels)` time and space.

## 22. Triangle rasterization **[ARK 438–444]**

For triangle `A,B,C` in screen space:

1. Compute and clamp its integer bounding box.
2. Test each pixel sample center against three oriented edge half-spaces.
3. Derive barycentric weights.
4. Interpolate depth and attributes.
5. Emit a fragment.

An oriented edge function is

$$
E_{AB}(P)=(B_x-A_x)(P_y-A_y)-(B_y-A_y)(P_x-A_x).
$$

For a consistently counterclockwise triangle, a point is inside when all three edge functions have the accepted sign. The sign depends on screen-y convention; verify once with a known interior point.

Barycentric weights can be computed as normalized edge functions:

$$
\alpha=\frac{E_{BC}(P)}{E_{BC}(A)},\quad
\beta =\frac{E_{CA}(P)}{E_{CA}(B)},\quad
\gamma=\frac{E_{AB}(P)}{E_{AB}(C)}.
$$

### Rasterization invariant and optimization

Edge functions are linear. Moving one pixel right or up changes each by a constant, so a rasterizer evaluates initial values then increments them—no repeated cross products per sample.

### Shared-edge/top-left rule

If two adjacent triangles both include their common boundary, double shading occurs; if both exclude it, cracks occur. Hardware uses a consistent rule such as “include top and left edges, exclude bottom and right edges.”

### Degenerate triangles

If signed twice-area `E_AB(C)` is zero (within tolerance), barycentric denominators vanish. Cull or treat the primitive as a line according to policy.

Bounding-box rasterization is `O(number of tested samples)`. Hardware organizes work in tiles/blocks and performs hierarchical rejection.

## 23. Line and polygon clipping

Clipping trims geometry to a permitted region. **Culling** discards whole primitives based on visibility or orientation; the terms are related but not interchangeable.

### Cohen–Sutherland line clipping

Assign each endpoint a 4-bit outcode relative to a rectangular window: left, right, bottom, top.

- `(code0 | code1)==0`: both inside, trivially accept.
- `(code0 & code1)!=0`: both share an outside half-space, trivially reject.
- Otherwise choose an outside endpoint, intersect with one indicated boundary, replace it, recompute its code, and repeat.

```cpp
enum { LEFT=1, RIGHT=2, BOTTOM=4, TOP=8 };

int outCode(double x, double y,
            double xmin, double xmax, double ymin, double ymax) {
    int c = 0;
    if (x < xmin) c |= LEFT; else if (x > xmax) c |= RIGHT;
    if (y < ymin) c |= BOTTOM; else if (y > ymax) c |= TOP;
    return c;
}

bool cohenSutherland(double& x0, double& y0, double& x1, double& y1,
                     double xmin, double xmax, double ymin, double ymax) {
    while (true) {
        int c0=outCode(x0,y0,xmin,xmax,ymin,ymax);
        int c1=outCode(x1,y1,xmin,xmax,ymin,ymax);
        if ((c0|c1)==0) return true;
        if ((c0&c1)!=0) return false;
        int c = c0 ? c0 : c1;
        double x=0,y=0;
        if (c & TOP) {
            if (y1==y0) return false;
            x=x0+(x1-x0)*(ymax-y0)/(y1-y0); y=ymax;
        } else if (c & BOTTOM) {
            if (y1==y0) return false;
            x=x0+(x1-x0)*(ymin-y0)/(y1-y0); y=ymin;
        } else if (c & RIGHT) {
            if (x1==x0) return false;
            y=y0+(y1-y0)*(xmax-x0)/(x1-x0); x=xmax;
        } else {
            if (x1==x0) return false;
            y=y0+(y1-y0)*(xmin-x0)/(x1-x0); x=xmin;
        }
        if (c==c0) { x0=x; y0=y; } else { x1=x; y1=y; }
    }
}
```

Outcodes make many accepts/rejects extremely cheap. Beware division by zero for horizontal or vertical segments and use tolerances in floating-point variants.

### Liang–Barsky line clipping

Parameterize `P(t)=P0+t(P1-P0)`, `0<=t<=1`. Each window inequality yields a constraint `p_i t <= q_i`. Maintain `t_enter=0`, `t_leave=1`:

- If `p_i=0` and `q_i<0`, the line is parallel and outside -> reject.
- If `p_i<0`, update entering bound `t_enter=max(t_enter,q_i/p_i)`.
- If `p_i>0`, update leaving bound `t_leave=min(t_leave,q_i/p_i)`.
- Accept iff `t_enter<=t_leave`.

For `[xmin,xmax] x [ymin,ymax]`:

```text
p = [-dx, dx, -dy, dy]
q = [x0-xmin, xmax-x0, y0-ymin, ymax-y0]
```

It usually performs fewer intersections than Cohen–Sutherland and directly returns the surviving parameter interval.

### Sutherland–Hodgman polygon clipping **[ARK 432–435]**

Clip a polygon against one convex clip-plane boundary at a time. For each directed polygon edge `S->E`:

- inside -> inside: output `E`;
- inside -> outside: output intersection;
- outside -> inside: output intersection, then `E`;
- outside -> outside: output nothing.

The output list becomes input to the next plane. The result remains a convex polygon when clipping a convex polygon against convex half-spaces. A clipped triangle may become a polygon with more than three vertices; triangulate it, e.g. as a fan.

For homogeneous plane function `d(P)=a x+b y+c z+d w`, edge intersection parameter is

$$
t=\frac{d(S)}{d(S)-d(E)},\qquad I=S+t(E-S).
$$

For `n` input vertices and `k` clip boundaries, time is `O(nk + output growth)`.

### Back-face culling **[ARK 425–436]**

Vertex order defines orientation. OpenGL traditionally treats counterclockwise winding as front-facing by default. A geometric test computes

$$
n=(v_1-v_0)\times(v_2-v_0)
$$

and compares it with a view direction. The exact `<0`/`>0` cull sign depends on whether the vector points surface-to-eye or eye-to-surface and on handedness. Say the convention rather than memorizing a naked sign.

Back-face culling can remove roughly half the triangles of a closed opaque mesh, but it is invalid for intentionally two-sided material or surfaces seen from inside unless configured accordingly. It does not replace depth testing: many front-facing surfaces still occlude each other.

---

# Part V — visibility, depth, and the GPU raster pipeline

## 24. Z-buffer visibility **[IJ 199–224; ARK 443; ARK 459–462]**

A z/depth buffer stores the closest accepted depth at each sample; the color/framebuffer stores its color. In the slide example, triangle B has `z=0.7`, triangle A has `z=0.2`, and smaller z is nearer. B is drawn first, then A replaces B only where A overlaps because `0.2<0.7`.

```text
for every sample (x,y):
    depth[x,y] = farthest_value
    color[x,y] = background

for each triangle T:
    rasterize every covered sample (x,y)
    interpolate z and attributes there
    if z is inside the valid depth range and z < depth[x,y]:
        depth[x,y] = z
        color[x,y] = shade(T, attributes)
```

The comparison may be `LESS`, `LEQUAL`, `GREATER`, etc.; reversed-z pipelines deliberately use an opposite convention for precision.

### Finding z at a sample

Methods include:

- barycentric interpolation of post-projection depth;
- the projected triangle plane equation;
- scanline interpolation: interpolate z to left/right scanline intersections, then increment z across pixels.

For vertex screen depths `z_A,z_B,z_C`:

$$
z_P=\alpha z_A+\beta z_B+\gamma z_C.
$$

The scanline version in the slides performs the same linear interpolation in two stages. For a scanline `y_s`, interpolate along two triangle edges to get `(x_a,z_a)` and `(x_b,z_b)`. Then, for a covered sample `x_p`,

$$
q=\frac{x_p-x_a}{x_b-x_a},\qquad z_p=(1-q)z_a+qz_b.
$$

Across a nonvertical span this can be updated incrementally with

$$
z(x+1)=z(x)+\frac{z_b-z_a}{x_b-x_a}.
$$

Horizontal/zero-width spans need an explicit endpoint rule to avoid division by zero; barycentric interpolation avoids special-casing the scanline construction while giving the same planar result.

Depth in window space is designed to interpolate linearly after projection. General attributes such as UVs require the perspective-correct formula given earlier.

### Complexity and properties

- Time: `O(total generated fragments)`.
- Space: `O(W H)` samples, multiplied by sample count under MSAA.
- It is generally independent of primitive submission order for opaque geometry, subject to equal-depth/tie and floating-point issues.
- It solves nearest-surface visibility, not transparency ordering.

### Depth precision and z-fighting

Perspective depth is nonlinear, with much more precision near the near plane. A very tiny near distance and huge far/near ratio waste precision and cause nearly coplanar surfaces to alternate visibility (**z-fighting**). Remedies: increase near, reduce far, use higher-precision depth, reversed-z with floating depth, or apply a carefully chosen polygon offset.

### Early z

Hardware may test depth before the fragment shader and skip expensive shading for occluded fragments. Writing a custom fragment depth, using certain discard/side effects, or other dependencies can disable or constrain early-z optimization.

## 25. Why rasterization is fast **[ARK 347–371]**

Real-time targets give a strict budget: 60 FPS means `1/60 s = 16.67 ms` for the whole frame; graphics may receive only about 10–12 ms after input and game logic.

Rasterization gains speed through:

- massive data parallelism across vertices/fragments;
- dedicated fixed-function rasterizers, interpolators, depth units, and render-output units;
- local lighting approximations instead of simulating every light bounce;
- precomputed data such as textures, environment maps, shadow maps, and light maps;
- predictable work roughly related to submitted/visible primitives and covered samples.

CPUs have fewer complex latency-optimized cores, large caches, branch prediction, and out-of-order execution. GPUs devote more hardware to many simpler throughput-oriented execution lanes. Graphics is a good match because the same shader runs independently on huge datasets. Divergent branches inside a GPU execution group reduce efficiency.

Historical arc in the slides: CPU software rendering -> fixed-function GPUs -> programmable vertex/fragment shaders -> unified programmable architectures and compute shaders. Modern ray-tracing hardware adds units for BVH traversal and ray-box/ray-triangle tests.

## 26. Modern graphics pipeline, stage by stage **[ARK 372–393; ARK 403–471]**

### Input assembly

Input assembly pulls vertex data from memory, interprets attribute layout, follows optional indices, and establishes primitive topology.

Typical vertex:

```text
position vec3 = 12 bytes
normal   vec3 = 12 bytes
UV       vec2 =  8 bytes
color    vec4 = 16 bytes
total         = 48 bytes
```

Primitive types include points, lines, and triangles. Triangles dominate because they are always planar, interpolate naturally, and are hardware-optimized.

Indexed drawing stores shared vertices once and lists index triples. For triangles `(A,B,C)` and `(B,C,D)`, non-indexed data stores six vertices; indexed data stores four vertices plus indices `0,1,2,1,2,3`. This reduces duplication and benefits the post-transform vertex cache, though a geometric corner may need duplicate vertices when normals or UV seams differ.

### Vertex shader

Runs once per submitted/reused vertex after assembly. It must output clip-space `gl_Position`; it may transform/passthrough normals, world positions, UVs, colors, skeletal animation results, and per-vertex lighting.

Coordinate chain with column vectors:

$$
p_{clip}=PVMp_{model}.
$$

The rightmost model matrix acts first.

### Optional tessellation

Substages:

1. tessellation control shader chooses subdivision levels;
2. fixed tessellator generates parameter/barycentric coordinates;
3. tessellation evaluation shader computes final vertex positions.

Uses: adaptive level of detail based on distance/screen size/curvature, smooth surfaces, and displacement mapping. It improves geometric detail but excessive tessellation creates tiny triangles and overhead.

### Optional geometry shader

Consumes complete primitives and may emit, modify, or discard primitives. A slide example converts a point into a camera-facing quad (**billboarding**) for particles, grass, leaves, sprites, or icons. Geometry shaders are flexible but often throughput-limited; instancing or compute-based generation may be faster.

### Primitive assembly, clipping, and culling

Vertices are grouped into primitives, winding establishes orientation, outside geometry is clipped to the view frustum, and configured faces may be culled.

### Rasterization

Covered sample locations are found, depth is generated, and attributes are interpolated. Output is fragments, not final pixels.

### Fragment shader

Runs for surviving fragment candidates and calculates output color(s), possibly depth. It can sample textures, apply lighting/material models, procedural effects, and post-processing. It may execute millions of times per frame and is often the most expensive programmable stage.

### Per-fragment operations

A conceptual order is:

```text
fragment -> scissor -> stencil -> depth -> blending -> framebuffer
```

Actual hardware can reorder compatible operations, especially early depth/stencil. Tests are fixed-function but configurable.

### Framebuffer output

A framebuffer is a collection of attachments:

- color buffers (e.g. RGBA8, RGBA16F; possibly multiple render targets);
- depth buffer (commonly 16/24/32-bit formats);
- stencil buffer (often 8 bits per sample).

It may be displayed or used off-screen as a texture/render target.

## 27. APIs and shader languages **[ARK 394–402]**

A graphics API is the application’s standardized interface to drivers/GPU hardware: it submits commands, configures pipeline state, allocates resources, and hides or exposes hardware detail.

- **OpenGL:** cross-platform, comparatively high-level, stable; legacy immediate/fixed-function mode is deprecated, modern retained rendering uses buffers and shaders.
- **Vulkan:** explicit, lower overhead, cross-platform; explicit synchronization/memory management and strong CPU parallel submission.
- **Direct3D:** Windows/Xbox graphics API, tightly integrated with that ecosystem.
- **Metal:** Apple’s low-overhead graphics/compute API.

Common shading representations/languages: GLSL for OpenGL, HLSL for Direct3D, MSL for Metal, and SPIR-V intermediate representation in Vulkan ecosystems.

GLSL storage qualifiers:

- `in`: input from vertex attributes or previous stage;
- `out`: output to next stage/framebuffer;
- `uniform`: read-only draw/dispatch parameters supplied outside individual shader invocations;
- `layout(location=...)`: explicit attribute/output location;
- `layout(binding=...)`: explicit resource binding point.

## 28. Runnable-style modern GLSL pair **[ARK 401–402; ARK 416; ARK 453–454]**

Vertex shader:

```glsl
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aUV;

out vec3 WorldPos;
out vec3 WorldNormal;
out vec2 UV;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vec4 world = model * vec4(aPos, 1.0);
    WorldPos = world.xyz;
    WorldNormal = normalize(transpose(inverse(mat3(model))) * aNormal);
    UV = aUV;
    gl_Position = projection * view * world;
}
```

Fragment shader using textured Blinn–Phong:

```glsl
#version 330 core
in vec3 WorldPos;
in vec3 WorldNormal;
in vec2 UV;
out vec4 FragColor;

uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 viewPos;
uniform sampler2D diffuseMap;

void main() {
    vec3 albedo = texture(diffuseMap, UV).rgb;
    vec3 N = normalize(WorldNormal);       // interpolation changes length
    vec3 L = normalize(lightPos - WorldPos);
    vec3 V = normalize(viewPos - WorldPos);
    vec3 H = normalize(L + V);

    vec3 ambient = 0.15 * albedo;
    float ndotl = max(dot(N, L), 0.0);
    vec3 diffuse = ndotl * albedo * lightColor;

    float spec = 0.0;
    if (ndotl > 0.0)
        spec = pow(max(dot(N, H), 0.0), 64.0);
    vec3 specular = spec * lightColor;

    FragColor = vec4(ambient + diffuse + specular, 1.0);
}
```

Focused multi-texture pattern from the slides:

```glsl
uniform sampler2D diffuseMap;
uniform sampler2D normalMap;
uniform sampler2D specularMap;
uniform sampler2D roughnessMap;

vec3 albedo = texture(diffuseMap, UV).rgb;
vec3 tangentNormal = texture(normalMap, UV).rgb * 2.0 - 1.0;
float specularStrength = texture(specularMap, UV).r;
float roughness = texture(roughnessMap, UV).r;

// TBN contains tangent, bitangent, and geometric normal as columns.
vec3 N = normalize(TBN * tangentNormal);
```

All samplers can use the same UV while supplying different material fields. The normal sample must be decoded from `[0,1]` to `[-1,1]` before the TBN transform. A one-channel map convention (`.r`) is common for specular strength and roughness. In a Phong-style model, convert roughness to a suitable shininess exponent rather than substituting it directly, because large Phong shininess means a narrow smooth highlight whereas large roughness means the opposite.

Shader traps:

- Forgetting to normalize interpolated normals.
- Calculating lighting with vectors in different coordinate spaces.
- Using `mat3(model)` for normals under nonuniform scaling.
- Applying lighting directly to gamma-encoded texture values instead of linear color.
- Treating `uniform` as “one value per vertex”; it is constant for the draw call/program use, not an interpolated attribute.

## 29. Flat, Gouraud, and Phong shading **[ARK 417; ARK 451–452]**

- **Flat shading:** one normal/intensity for the whole face; visibly faceted, cheapest.
- **Gouraud shading:** compute lighting per vertex and interpolate colors. Fast, but a small specular highlight entirely inside a triangle can disappear because no vertex samples it.
- **Phong shading:** interpolate normals (and positions), renormalize, then compute illumination per fragment. It produces smoother, more accurate highlights at higher cost.

Do not confuse **Phong illumination model** (ambient + diffuse + specular equation) with **Phong shading** (where the equation is evaluated per fragment).

## 30. Blending, stencil, double buffering, and VSync **[ARK 458–471]**

### Standard alpha blending

For straight/unassociated alpha:

$$
C_{out}=\alpha_s C_s+(1-\alpha_s)C_d.
$$

Common modes:

- Additive: `C_out=C_s+C_d` for fire/light/particles.
- Multiplicative: `C_out=C_s*C_d` for darkening/filtering.
- Screen: `C_out=1-(1-C_s)(1-C_d)` for brightening.

Transparency is order-dependent. Standard transparent objects are normally sorted back-to-front after opaque objects; depth writes are usually disabled for that pass while depth testing stays enabled. Order-independent transparency uses more advanced methods.

Premultiplied alpha stores `alpha*C` and uses `C_out=C_s+(1-alpha_s)C_d`; it behaves better at filtered transparent edges when the entire pipeline is consistent.

### Stencil and scissor

- Scissor discards fragments outside a configured rectangle; useful for UI and viewport masking.
- Stencil stores small per-sample integers and conditionally passes/updates them; uses include outlines, mirrors, portals, shadow volumes, and masks.

### Double buffering

Render a complete frame into a back buffer while the front buffer is displayed; atomically swap when ready. This prevents the user from seeing a partially rendered frame and reduces flicker. It alone does not guarantee no tear if swapping occurs mid-refresh.

### VSync

VSync synchronizes presentation with display refresh. At 60/120/144 Hz, refresh intervals are approximately 16.67/8.33/6.94 ms. It prevents tearing and stabilizes timing but can cap frame rate and increase input latency. Adaptive refresh technologies reduce this trade-off.

---

# Part VI — color, light, material, and texture

## 31. Light as a physical and computational quantity **[ARK 159–171]**

Light is electromagnetic radiation. Wavelength distribution influences perceived color; radiometric intensity influences brightness. At a surface, energy may be reflected, absorbed (often becoming heat), or transmitted.

Graphics cannot track every photon in a complex world directly under normal budgets. Raster systems approximate local illumination; ray/path tracers sample selected light-transport paths.

Distinguish these terms:

- **Illumination/lighting model:** computes light interaction at a point.
- **Shading:** how that model is evaluated/interpolated across a primitive.
- **Material:** coefficients/textures describing surface response.
- **Radiance:** directional light-flow quantity central to physically based rendering.

## 32. Color representations and gamma — viva-critical supplement

### RGB

RGB is an additive device-oriented model. Black is `(0,0,0)` and ideal full white is `(1,1,1)`. Displays emit red, green, and blue primaries; a framebuffer commonly stores them plus alpha.

### CMY/CMYK

Ideal subtractive conversion for normalized RGB is

$$
C=1-R,\quad M=1-G,\quad Y=1-B.
$$

Printing adds black `K` for density/economy and because real inks are not ideal. One common conversion sets `K=min(C,M,Y)` then rescales remaining components; exact color management depends on device profiles.

### HSV/HSL

HSV/HSL reorganize RGB into hue plus saturation and a brightness/lightness component. They are convenient for user selection and editing, not physically uniform color spaces. Hue becomes undefined/irrelevant when saturation is zero.

### Linear light versus sRGB/gamma encoding

Most stored/display RGB is nonlinear (e.g. sRGB) so code values match human perceptual sensitivity. Physical operations—lighting, interpolation intended to represent energy, filtering, and blending—should be performed in **linear** color:

```text
sRGB texture -> decode to linear -> shade/blend/filter -> encode to sRGB display
```

Adding `0.5 sRGB + 0.5 sRGB` as if values were linear is not generally physically correct. Modern APIs can automatically decode sRGB textures and encode sRGB framebuffers when formats/state are correct.

### Alpha is not transparency by itself

Alpha is coverage/opacity data interpreted by a composition equation. An RGBA tuple does not become transparent unless blending/compositing is enabled and consistently defined.

## 33. Light-source models **[ARK 169–206]**

### Point light

For surface point `P`, light position `P_l`, and RGB intensity `I_l`:

$$
L=P_l-P,\qquad d=\lVert L\rVert,\qquad \hat L=L/d.
$$

Energy from an ideal isotropic point source spreads over sphere area `4 pi d²`, giving inverse-square falloff:

$$
I(P)\propto\frac{I_l}{d^2}.
$$

The slides use a numerical guard:

$$
I_{final}=\frac{I_l}{\epsilon+d^2}.
$$

Real-time systems also use a tunable form

$$
atten(d)=\frac1{k_c+k_ld+k_qd^2}.
$$

Do not silently normalize `L` before saving its length; attenuation needs distance.

### Directional light

A distant source such as the sun is approximated by parallel rays. If `D_l` is the normalized direction **the light rays travel**, direction from surface to light is `L=-D_l`. Intensity and direction are constant across the scene; there is no distance attenuation.

### Spotlight

Spotlight has point position `S`, central direction `D_spot`, cutoff angle `theta_c`, and falloff exponent `e`. If `L` points from surface to light, the vector from light to surface is `-L`:

$$
\cos\alpha=D_{spot}\cdot(-\hat L).
$$

Inside the cone when

$$
\cos\alpha>\cos\theta_c.
$$

Comparing cosines avoids `acos`; note cosine decreases over `[0,pi]`, so the inequality direction matters.

Hard-edged slide factor:

$$
spot(\alpha)=
\begin{cases}
(\cos\alpha)^e,&\cos\alpha>\cos\theta_c\\
0,&otherwise.
\end{cases}
$$

Combine with distance attenuation. Larger `e` concentrates brightness toward the axis. Production shading often uses inner and outer cutoff cosines with `smoothstep` to avoid a hard boundary.

### Ambient light

Ambient light is a cheap constant approximation to indirect illumination. It prevents completely black unlit regions but is not a real global-illumination solution; it has no spatial/directional occlusion knowledge. Ambient occlusion or environment lighting gives more plausible variation.

## 34. Surface normals **[ARK 207–213]**

A surface normal is perpendicular to the local tangent plane and normally normalized.

- Triangle: `normalize((B-A)×(C-A))`.
- Sphere centered at `C`: `normalize(P-C)`.
- Plane `Ax+By+Cz+D=0`: `normalize(A,B,C)`.
- Implicit surface `F(x,y,z)=0`: `normalize(grad F(P))`, assuming nonzero gradient.
- Parametric surface `S(u,v)`: `normalize(S_u × S_v)`.

The normal orientation changes if triangle winding/cross-product order changes. Smooth meshes may store vertex normals and interpolate them; hard edges require split normals/vertices.

### Specular, diffuse, and ambient reflection **[ARK 218–221]**

| Component | Surface intuition | Direction/view behavior | Visible effect |
|---|---|---|---|
| Specular | smooth or mirror-like surface | concentrated around the reflection direction; view-dependent | sharp or glossy highlight/reflection |
| Diffuse | rough or matte surface such as paper, clay, or fabric | ideal Lambert response depends on `N·L`, not viewing direction | broadly scattered matte color |
| Ambient | simplified stand-in for indirect illumination | constant/view-independent in the basic Phong model | prevents unlit regions from becoming completely black |

Real surfaces usually combine the three terms. “Ambient reflection” in this local model is a computational approximation, not a physically complete simulation of all interreflection. A perfect mirror is an extreme directional specular case; Phong’s powered cosine is a glossy empirical approximation.

## 35. Phong illumination model **[ARK 214–245]**

The Phong model is an empirical local model with ambient, Lambertian diffuse, and glossy specular components:

$$
I=I_{ambient}+I_{diffuse}+I_{specular}.
$$

Assume normalized `N` (surface normal), `L` (surface-to-light), `V` (surface-to-viewer), and `R=2(N·L)N-L`.

### Ambient

$$
I_a=k_a\odot I_{ambient}.
$$

`⊙` means component-wise RGB multiplication.

### Lambert diffuse

$$
I_d=k_d\odot I_l\max(0,N\cdot L).
$$

Why cosine? An oblique beam distributes roughly the same energy over area enlarged by `1/cos(theta)`, so energy per unit area scales by `cos(theta)`. Lambertian reflected appearance is view-independent.

### Phong specular

$$
I_s=k_s\odot I_l[\max(0,R\cdot V)]^n.
$$

`n` is the shininess exponent. Larger `n` creates a narrower, sharper highlight; `k_s` controls its strength/color. Normally calculate specular only when `N·L>0` so a light behind the surface cannot create a highlight.

For multiple lights:

$$
I=k_a\odot I_a+
\sum_i attenuation_i\,visibility_i\, I_{l_i}\odot
\left[k_d\max(0,N\cdot L_i)+k_s\max(0,R_i\cdot V)^n\right].
$$

Clamp/tone-map only at the appropriate later stage; prematurely clamping each light loses energy.

### Worked numeric example

Let `N=(0,0,1)`, `L=(0,0,1)`, `V=(0,0,1)`, `k_a=0.1`, `k_d=0.7`, `k_s=0.2`, white unit light/ambient, and any positive `n`.

```text
N·L = 1
R = 2N - L = N
R·V = 1
I = 0.1 + 0.7 + 0.2 = 1.0 per channel
```

If L is tangent, `N·L=0`; diffuse is zero and specular should also be suppressed by the front-light condition.

## 36. Blinn–Phong **[ARK 246–250]**

Instead of constructing `R`, use halfway direction

$$
H=\frac{L+V}{\lVert L+V\rVert}
$$

and

$$
I_s=k_s\odot I_l[\max(0,N\cdot H)]^{n'}.
$$

When `V=R`, `H=N`. To approximate a Phong lobe, the Blinn exponent is commonly a few times larger (the slides say roughly 2–4 times). There is no universal exact conversion for every angle convention.

Edge case: `L≈-V` makes `L+V≈0`, so H cannot be normalized; specular is effectively absent or handled safely.

## 37. Texture mapping **[ARK 251–261]**

A texture is data indexed by surface coordinates. It may encode albedo/color, normal direction, specular strength, roughness, opacity, height, displacement, or other material fields.

### UV parameterization

Each mesh vertex normally has position `(x,y,z)` and texture coordinate `(u,v)`. For a triangle, barycentric interpolation gives interior UVs—but use perspective-correct interpolation after projection.

Typical convention is `u,v in [0,1]`; image/API origins can differ (top-left versus bottom-left), so a vertical flip may be required.

Mapping examples:

- Spherical: `u=phi/(2pi)` and `v=theta/pi`, with angle-offset/sign conventions chosen for axes.
- Cylindrical: `u=phi/(2pi)`, `v=(z-z_min)/(z_max-z_min)`.
- Cube mapping: choose a face from dominant direction component, then derive face-local 2D coordinates.

Every global parameterization has distortion or seams; UV unwrapping trades among angle, area, boundary, and continuity distortion.

### Nearest and bilinear filtering

For a `W x H` texture, let `x=u(W-1)`, `y=v(H-1)` after address handling.

Nearest:

```text
T[round(x), round(y)]
```

Bilinear uses four texels. Let `x0=floor(x)`, `y0=floor(y)`, `a=x-x0`, `b=y-y0`:

$$
c=lerp(lerp(c_{00},c_{10},a),lerp(c_{01},c_{11},a),b).
$$

It is linear in one axis followed by the other. Handle `x0+1` and `y0+1` according to address mode rather than reading out of bounds.

Address modes:

- repeat: wrap fractional coordinate;
- clamp: pin to the edge;
- mirrored repeat: alternate direction each tile;
- border: return a configured outside color.

### Minification, mipmaps, and anisotropy

When many texels map to one pixel, nearest/bilinear sampling aliases. A mipmap stores successively low-pass-filtered half-resolution levels. Choose level from screen-space texture derivatives; trilinear filtering interpolates between bilinear samples from two neighboring levels. Anisotropic filtering takes more direction-aware samples for footprints stretched at grazing angles.

### Texture types from the slides

- Albedo: `k_d(u,v)=T_albedo(u,v)`.
- Specular: `k_s(u,v)=T_specular(u,v)`.
- Roughness/shininess: material exponent varies over the surface; note physically based roughness and Phong shininess are inversely related rather than literally identical.
- Height/displacement: move actual position `P'=P+h(u,v)N`; silhouette and geometry can change.
- Normal map: perturbs shading normal without adding actual geometry; silhouette is unchanged.

### Tangent-space normal mapping

Construct tangent `T`, bitangent `B`, and normal `N`; with UV parameterization, conceptually `T=partial P/partial u`, `B=partial P/partial v`. Decode RGB normal map:

$$
n_{map}=2T_{normal}(u,v)-1.
$$

Then

$$
n_{world}=normalize([T\ B\ N]\,n_{map}).
$$

In real meshes, orthonormalize T against N and preserve handedness for B. A flat tangent-space normal is usually approximately `(0,0,1)`, hence normal maps look predominantly blue.

---

# Part VII — ray casting, ray tracing, and path tracing

## 38. From physical light to reverse ray casting **[ARK 1–31]**

Physical photons leave sources, undergo surface interactions, and only a tiny subset enters the eye. Forward-simulating every emitted photon wastes enormous work. Ray casting reverses the question:

1. place an image plane in front of the eye;
2. send a primary ray through each pixel sample;
3. find its closest visible surface;
4. calculate that sample’s color.

This reduces infinitely many possible light paths to a finite set driven by image samples. Reverse rays are a computational construction; light itself does not physically travel backward in time.

## 39. Ray and hit-record invariants **[ARK 32–39]**

$$
P(t)=O+td,\qquad t\ge0.
$$

A renderer usually passes an interval `[t_min,t_max]` and a hit record containing:

```cpp
struct Hit {
    double t;
    Vec3 p;
    Vec3 normal;
    Material* material;
    double u, v;        // texture coordinates
    bool frontFace;
};
```

Nearest-hit invariant: while visiting objects, `t_max` is the nearest accepted `t` so far. A candidate is accepted only when `t_min<=t<t_max`, then `t_max` shrinks. This makes traversal order irrelevant to final opaque visibility.

Choose the outward normal and orient it consistently:

```cpp
hit.frontFace = dot(ray.direction, outwardNormal) < 0;
hit.normal = hit.frontFace ? outwardNormal : -outwardNormal;
```

## 40. Ray-triangle intersection **[ARK 40–60]**

### Two-step method

1. Intersect ray with the triangle’s plane.
2. Compute barycentric coordinates and test nonnegative bounds.

This is intuitive but can repeat work.

### Direct system

Set ray and barycentric forms equal:

$$
O+td=A+\beta(B-A)+\gamma(C-A).
$$

Rearrange:

$$
[-d\quad B-A\quad C-A]
\begin{bmatrix}t\\\beta\\\gamma\end{bmatrix}=O-A.
$$

Solve by Cramer’s rule/LU for a conceptual derivation. In practice, Möller–Trumbore is an efficient determinant form:

```cpp
bool hitTriangle(Vec3 O, Vec3 d, Vec3 A, Vec3 B, Vec3 C,
                 double tMin, double tMax,
                 double& t, double& beta, double& gamma) {
    const double eps = 1e-9;
    Vec3 e1 = B - A, e2 = C - A;
    Vec3 p = cross(d, e2);
    double det = dot(e1, p);
    if (std::abs(det) < eps) return false; // parallel or degenerate
    double invDet = 1.0 / det;
    Vec3 s = O - A;
    beta = dot(s, p) * invDet;
    if (beta < 0.0 || beta > 1.0) return false;
    Vec3 q = cross(s, e1);
    gamma = dot(d, q) * invDet;
    if (gamma < 0.0 || beta + gamma > 1.0) return false;
    t = dot(e2, q) * invDet;
    return t >= tMin && t <= tMax;
}
```

`alpha=1-beta-gamma`. These weights interpolate UVs, normals, and colors “for free.” For one-sided triangles, determinant sign can also perform back-face culling instead of using `abs(det)`.

Time and extra space are `O(1)`. Degenerate/near-parallel triangles need an epsilon scaled sensibly to the scene.

## 41. Ray-sphere intersection **[ARK 61–75]**

Sphere center `C`, radius `r`:

$$
(P-C)\cdot(P-C)-r^2=0.
$$

Let `oc=O-C`, substitute `P=O+td`:

$$
at^2+bt+c=0
$$

with

$$
a=d\cdot d,\quad b=2(oc\cdot d),\quad c=oc\cdot oc-r^2.
$$

Discriminant `Delta=b²-4ac`:

- `Delta<0`: no real intersection;
- `Delta=0`: tangent;
- `Delta>0`: two line intersections.

Test the smaller root first, then the larger, because the smaller may be behind/under `t_min` when the ray begins inside the sphere.

```cpp
bool hitSphere(Vec3 O, Vec3 d, Vec3 C, double r,
               double tMin, double tMax, double& t) {
    Vec3 oc = O - C;
    double a = dot(d,d);
    double halfB = dot(oc,d); // b/2, improves compactness
    double c = dot(oc,oc) - r*r;
    double disc = halfB*halfB - a*c;
    if (disc < 0) return false;
    double rootDisc = std::sqrt(std::max(0.0, disc));
    double root = (-halfB - rootDisc) / a;
    if (root < tMin || root > tMax) {
        root = (-halfB + rootDisc) / a;
        if (root < tMin || root > tMax) return false;
    }
    t = root;
    return true;
}
```

### Geometric method from the slides

For normalized d, let vector from origin to center be `C-O`. Projection to closest ray point:

$$
t_p=(C-O)\cdot d.
$$

If origin is outside and `t_p<0`, reject early. Closest squared center distance:

$$
d_\perp^2=\lVert C-O\rVert^2-t_p^2.
$$

Reject if `d_perp²>r²`. Otherwise half-chord distance

$$
t'=\sqrt{r^2-d_\perp^2},
$$

and roots are `t_p-t'` and `t_p+t'`. Choose the closest valid interval root. If d is not unit, this exact distance interpretation must be adjusted.

## 42. Ray-general-quadric intersection **[ARK 76–80]**

General quadric:

$$
Ax^2+By^2+Cz^2+Dxy+Eyz+Fxz+Gx+Hy+Iz+J=0.
$$

Substitute `x=O_x+td_x`, etc. Collect coefficients of `t²,t,1`, solve the quadratic, and keep the nearest valid real root. Explicitly:

$$
a=Ad_x^2+Bd_y^2+Cd_z^2+Dd_xd_y+Ed_yd_z+Fd_xd_z,
$$

$$
\begin{aligned}
b={}&2AO_xd_x+2BO_yd_y+2CO_zd_z\\
&+D(O_xd_y+O_yd_x)+E(O_yd_z+O_zd_y)\\
&+F(O_xd_z+O_zd_x)+Gd_x+Hd_y+Id_z,
\end{aligned}
$$

$$
c=AO_x^2+BO_y^2+CO_z^2+DO_xO_y+EO_yO_z+FO_xO_z+GO_x+HO_y+IO_z+J.
$$

If `|a|` is nearly zero, it reduces to a linear equation `bt+c=0`; do not blindly divide by `2a`. Quadrics include ellipsoid, cylinder, cone, paraboloid, and hyperboloid forms. Normal at hit is the normalized gradient of the implicit quadric.

## 43. Ray-AABB slab intersection **[ARK 81–93]**

An axis-aligned bounding box is stored by `B_min=(xmin,ymin,zmin)` and `B_max=(xmax,ymax,zmax)`. Each axis defines a slab. For axis `i`:

$$
t_0=\frac{B_{min,i}-O_i}{d_i},\qquad
t_1=\frac{B_{max,i}-O_i}{d_i}.
$$

Swap if `t0>t1`. Intersect all parameter intervals:

$$
t_{enter}=\max_i t_{0i},\qquad
t_{exit}=\min_i t_{1i}.
$$

Hit iff `t_enter<=t_exit` and the interval overlaps the usable ray interval.

```cpp
bool hitAABB(Vec3 O, Vec3 d, Vec3 bmin, Vec3 bmax,
             double tMin, double tMax) {
    for (int axis=0; axis<3; ++axis) {
        if (std::abs(d[axis]) < 1e-12) {
            if (O[axis] < bmin[axis] || O[axis] > bmax[axis])
                return false;               // parallel and outside slab
            continue;                       // interval is (-inf,+inf)
        }
        double t0=(bmin[axis]-O[axis])/d[axis];
        double t1=(bmax[axis]-O[axis])/d[axis];
        if (t0>t1) std::swap(t0,t1);
        tMin=std::max(tMin,t0);
        tMax=std::min(tMax,t1);
        if (tMin>tMax) return false;
    }
    return true;
}
```

The slides note relying on IEEE infinity can handle some zero divisions, but explicit parallel-slab handling is clearer and avoids `0/0` NaNs exactly on a boundary. Time/space are `O(1)`.

## 44. Ray casting versus recursive ray tracing **[ARK 131–145]**

- **Ray casting:** primary rays only; nearest surface plus a local shading decision.
- **Recursive ray tracing:** adds secondary rays for shadow, reflection, and refraction effects.

Ray types:

1. primary: camera -> scene;
2. shadow: surface hit -> light;
3. reflection: surface hit along mirror reflection;
4. refraction/transmission: surface hit through transparent material.

### Shadow ray

For point light at `Lpos` and hit `P`:

```text
toLight = Lpos - P
distance = |toLight|
direction = toLight / distance
origin = P + epsilon*N
occluded iff any hit has epsilon < t < distance-epsilon
```

For a directional light, `t_max` is effectively infinity. A binary shadow ray produces a hard shadow for a point light; soft shadows require sampling an area light at multiple positions.

### Mirror reflection

With incident ray direction `I` toward the surface:

$$
R=I-2(I\cdot N)N.
$$

Blend local and reflected contributions according to a material coefficient `k_r`; physically meaningful renderers conserve energy rather than arbitrarily adding unlimited components.

### Refraction

Snell’s law:

$$
\eta_i\sin\theta_i=\eta_t\sin\theta_t.
$$

Let `eta=eta_i/eta_t`, unit incident `I`, oriented normal `N`, and `cos_i=min(-I·N,1)`:

$$
r_{out,\perp}=\eta(I+\cos_iN),
$$

Let

$$
k=1-\lVert r_{out,\perp}\rVert^2.
$$

If `k<0`—equivalently `eta*sin(theta_i)>1`—no real transmitted direction exists: **total internal reflection**. Do not take an absolute value, which would fabricate a refracted ray. Otherwise,

$$
r_{out,\parallel}=-\sqrt{\max(0,k)}\,N,
$$

where `max(0,k)` only suppresses a tiny negative roundoff error after the physical `k<0` test. Then `r_out=r_out,perp+r_out,parallel`. Fresnel reflectance makes grazing angles more reflective; Schlick approximation is

$$
R(\theta)=R_0+(1-R_0)(1-\cos\theta)^5,
\quad
R_0=\left(\frac{\eta_i-\eta_t}{\eta_i+\eta_t}\right)^2.
$$

### Epsilon/self-intersection problem

Floating-point hit position may lie microscopically below/above the theoretical surface. A secondary ray can immediately hit its source surface, causing acne, false shadows, or trapped rays. Start at `P+epsilon*N` in the appropriate side or set `t_min=epsilon`.

Too small leaves acne; too large causes light leaks/detached shadows. A scale-aware offset based on position magnitude and numerical error is better than one universal magic constant.

### Recursive trace pseudocode

```cpp
Color trace(const Ray& ray, int depth) {
    if (depth <= 0) return {0,0,0};
    Hit h;
    if (!scene.closestHit(ray, EPS, INF, h))
        return environment(ray.direction);

    Color result = localIllumination(h); // includes visibility tests

    if (h.material.reflectivity > 0) {
        Vec3 R = reflect(normalize(ray.direction), h.normal);
        result += h.material.reflectivity *
                  trace({h.p + EPS*h.normal, R}, depth-1);
    }

    // Refracted branch, Fresnel weighting, etc. may be added here.
    return result;
}
```

Termination: maximum depth and/or negligible throughput. In path tracing, Russian roulette gives probabilistic termination without systematically biasing long-path contribution.

Naive branching may grow exponentially with depth if every hit spawns several child rays. In simple Whitted tracing, the maximum theoretical count is geometric in branches, though many branches terminate early.

## 45. Acceleration and BVH **[ARK 146–152]**

With `R` rays and `N` objects, naive traversal performs `O(RN)` primitive tests. For millions of triangles and rays this dominates render time.

A **Bounding Volume Hierarchy** is a tree whose node bounds all primitives below it:

1. compute bounds for a primitive set;
2. choose split axis, often the longest extent;
3. partition primitives by centroid (median, spatial split, or SAH);
4. recursively build children until a leaf threshold;
5. during traversal, test the node AABB first and skip a missed subtree.

```text
traverse(node, ray, currentClosest):
    if ray misses node.box before currentClosest: return no hit
    if leaf:
        test its primitives, shrink currentClosest on hits
    else:
        visit nearer child first
        visit farther child only if its box can beat currentClosest
```

Complexity nuance:

- Balanced, spatially coherent BVH traversal is often approximately logarithmic plus actual nearby candidates.
- Worst case is still `O(N)` when bounds overlap badly or the tree is poor. Saying “always O(log N)” is incorrect.
- Median construction with sorting at every level is `O(N log²N)` in a simple implementation; presorting/linear partition strategies can reach `O(N log N)`.
- SAH estimates traversal/intersection cost using child surface areas; it costs more to build but often renders faster.

Dedicated ray-tracing hardware accelerates BVH traversal and ray-box/ray-triangle intersections. Shader cores still perform material evaluation; tensor/AI hardware may assist denoising. Hardware changes speed, not the mathematical definition of a ray hit.

## 46. Rendering equation and path tracing **[ARK 153–158]**

The rendering equation at surface point `P` is

$$
L_o(P,\omega_o,\lambda)=L_e(P,\omega_o,\lambda)+
\int_{\Omega} f_r(P,\omega_i,\omega_o,\lambda)
L_i(P,\omega_i,\lambda)
\max(0,N\cdot\omega_i)\,d\omega_i.
$$

- `L_o`: outgoing radiance toward viewer;
- `L_e`: emitted radiance;
- `L_i`: incoming radiance from direction `omega_i`;
- `f_r`: BRDF/material scattering response;
- `Omega`: hemisphere above the surface;
- cosine term: projected-area factor.

The integral contains infinitely many directions and recursively depends on light arriving from other surfaces. Path tracing estimates it by Monte Carlo sampling. For samples `omega_k` drawn from density `p(omega)`:

$$
\int g(\omega)d\omega
\approx\frac1N\sum_{k=1}^N\frac{g(\omega_k)}{p(\omega_k)}.
$$

```text
pathTrace(ray):
    throughput = 1
    radiance = 0
    repeat for bounces:
        hit = closest intersection
        if miss: radiance += throughput * environment; stop
        radiance += throughput * emitted(hit)
        optionally sample lights directly (next-event estimation)
        sample a new direction from the material BSDF
        throughput *= BSDF * cosine / samplePDF
        after several bounces, use Russian roulette
```

Classic recursive/Whitted ray tracing emphasizes deterministic perfect reflection/refraction plus direct lighting. Path tracing samples full light transport and can produce global illumination, soft shadows, color bleeding, caustic paths (though difficult), and depth of field. A correct Monte Carlo estimator can be unbiased, but finite samples are noisy; denoising or more samples reduce visible variance. “Unbiased” does not mean “noise-free.”

---

# Part VIII — sampling and anti-aliasing

## 47. Why aliasing occurs

Rasterization samples a continuous image at discrete locations. Frequencies above what the sampling grid can represent masquerade as false lower frequencies (**aliasing**): jagged edges, moiré texture patterns, shimmering, and temporal flicker.

Nyquist principle: a band-limited signal must be sampled at more than twice its highest frequency to reconstruct it. Real scene edges are not band-limited, so rendering must filter their high frequencies rather than merely sample harder.

## 48. Spatial anti-aliasing methods

- **Supersampling/SSAA:** render multiple samples per pixel (or a larger image), low-pass filter, then downsample. High quality, shades each sample, expensive.
- **MSAA:** store multiple coverage/depth samples per pixel but often shade fewer times; effective for polygon edges, not enough for shader/texture aliasing inside a triangle.
- **Analytic coverage:** compute how much of a pixel footprint a primitive covers.
- **Post-process AA (FXAA/SMAA):** detect/filter visible edges after rendering; inexpensive but may blur details and cannot recover lost subpixel information.
- **Temporal AA:** jitter sample positions across frames and accumulate motion-compensated history; powerful, but bad reprojection/history rejection causes ghosting.

Sample positions should be distributed, not all duplicated at the center. Random sampling turns structured aliasing into noise; stratified/low-discrepancy patterns reduce variance.

## 49. Texture anti-aliasing

Minification requires averaging a texture footprint, not choosing one texel. Mipmaps prefilter approximately square footprints; trilinear interpolation hides level transitions; anisotropic filtering handles elongated footprints at grazing views. Magnification filtering (nearest/bilinear) solves blockiness/smoothness but not minification aliasing.

## 50. Ray-tracing anti-aliasing

Trace multiple rays at subpixel positions and average:

$$
C_{pixel}\approx\frac1N\sum_{k=1}^NC(ray(x_k,y_k)).
$$

The same sampling framework supports depth of field, motion blur, area-light soft shadows, and Monte Carlo path tracing. Error decreases statistically around `O(1/sqrt(N))`, so four times as many independent samples roughly halves standard deviation—not quarters it.

---

# Part IX — parametric curves and surfaces

## 51. Raster versus vector and parametric form **[IJ 225–239]**

Raster images store pixels and reveal pixels under enlargement. Vector art/fonts store geometric curves and are rasterized at the requested scale.

Explicit `y=f(x)` cannot represent vertical lines or multiple y values at one x. Implicit `F(x,y)=0` represents shapes broadly but is not always easy to traverse in a chosen direction. A parametric curve uses

$$
P(t)=(x(t),y(t),z(t)).
$$

It represents loops/vertical tangents, provides direction and derivatives, and is natural for animation and sampling.

Nuance: equal increments of `t` are easy, but do **not** necessarily produce equal arc-length spacing unless speed `|P'(t)|` is constant. Uniform-distance animation needs arc-length reparameterization or an approximation table.

Applications from the slides: TrueType/OpenType fonts, SVG/logo/UI design, motion and camera paths, keyframe interpolation/easing, NURBS/CAD surfaces, game models, and architecture.

## 52. LERP and parametric lines **[IJ 234–236]**

$$
P(t)=P_0+t(P_1-P_0)=(1-t)P_0+tP_1.
$$

For `0<=t<=1` this is the segment; `t=0.5` is the midpoint. Outside that range it extrapolates.

```python
def lerp(a, b, t):
    return (1.0 - t) * a + t * b
```

LERP is affine-invariant and component-wise. For 3D rotations, linearly interpolating Euler angles or matrices can give poor/nonrigid motion; use quaternion SLERP for orientation.

## 53. Polynomial curves and continuity **[IJ 237–243]**

Polynomial vector curve:

$$
P(t)=a_0+a_1t+a_2t^2+\cdots+a_nt^n.
$$

Raw power-basis coefficients have weak geometric meaning, and a coefficient change affects the whole curve. Piecewise curves improve control, but joints require continuity conditions.

- `C0`: positions match, `P1(1)=P2(0)`; connected but can kink.
- `C1`: positions and first derivatives match; same tangent vector and parameter speed.
- `C2`: positions, first derivatives, and second derivatives match; smoother curvature behavior.
- `G1` (useful supplement): tangent **directions** match, but magnitudes may differ. It looks tangent-continuous while not necessarily C1.

The slide labels C2 as curvature match; strictly, matching first and second parameter derivatives implies strong smoothness, while geometric curvature also depends on their combination.

## 54. Bézier curves and de Casteljau **[IJ 244–258]**

### Quadratic

For control points `P0,P1,P2`:

$$
B(t)=(1-t)^2P_0+2t(1-t)P_1+t^2P_2.
$$

It is a LERP of LERPs:

$$
Q_0=lerp(P_0,P_1,t),\quad Q_1=lerp(P_1,P_2,t),
$$

$$
B=lerp(Q_0,Q_1,t).
$$

### Cubic

$$
B(t)=(1-t)^3P_0+3t(1-t)^2P_1+3t^2(1-t)P_2+t^3P_3.
$$

### General degree n

$$
B(t)=\sum_{i=0}^{n}B_{i,n}(t)P_i,
$$

$$
B_{i,n}(t)={n\choose i}t^i(1-t)^{n-i}.
$$

Bernstein basis properties on `[0,1]`:

- nonnegative;
- partition of unity: `sum_i B_i,n(t)=1` by the binomial theorem;
- therefore every curve point is a convex combination of controls.

Consequences:

- endpoint interpolation: `B(0)=P0`, `B(1)=Pn`;
- curve lies in the convex hull of its control points;
- affine invariance: transform control points, and the whole curve transforms identically;
- predictable stability/bounds.

Endpoint derivatives:

$$
B'(0)=n(P_1-P_0),\qquad B'(1)=n(P_n-P_{n-1}).
$$

Thus first/last control-polygon edges set endpoint tangent directions.

### De Casteljau evaluator

```python
def bezier(points, t):
    """points are numeric vectors supporting + and scalar *."""
    q = list(points)
    n = len(q)
    for level in range(1, n):
        for i in range(n - level):
            q[i] = (1.0 - t) * q[i] + t * q[i + 1]
    return q[0]
```

Time is `O(n²)` and in-place extra space is `O(n)`. It is numerically stable and its triangular intermediate points split the curve at `t` into two exact Bézier curves.

### Joining cubic Béziers

For first controls `P0..P3` and second `Q0..Q3`:

- C0: `P3=Q0`.
- C1 with the same parameter scale: `Q1-Q0=P3-P2`.
- G1: those vectors only need to be positive scalar multiples.
- C2 additionally matches `P3-2P2+P1 = Q2-2Q1+Q0` under the same parameterization.

## 55. Cubic Bézier matrix form **[IJ 259–261]**

Using row parameter vector `T=[1,t,t²,t³]` and column control vector `P=[P0,P1,P2,P3]^T`:

$$
B(t)=T M_B P,
$$

$$
M_B=\begin{bmatrix}
1&0&0&0\\
-3&3&0&0\\
3&-6&3&0\\
-1&3&-3&1
\end{bmatrix}.
$$

```python
import numpy as np

def cubic_bezier(t, control_points):
    T = np.array([1.0, t, t*t, t*t*t])
    M = np.array([[ 1,  0,  0, 0],
                  [-3,  3,  0, 0],
                  [ 3, -6,  3, 0],
                  [-1,  3, -3, 1]], dtype=float)
    P = np.asarray(control_points, dtype=float)
    return T @ M @ P
```

Derivative follows from `T'=[0,1,2t,3t²]`. Matrix form maps well to batched/GPU calculation, though de Casteljau is typically more stable for evaluation/subdivision.

## 56. Bézier surfaces, B-splines, and NURBS — viva-critical surface supplement

### Tensor-product Bézier patch

For control net `P_ij`, degrees `m,n`:

$$
S(u,v)=\sum_{i=0}^{m}\sum_{j=0}^{n}
B_{i,m}(u)B_{j,n}(v)P_{ij}.
$$

Surface tangents are partial derivatives `S_u,S_v`; normal is

$$
N=normalize(S_u\times S_v).
$$

The patch lies in the convex hull of its control net and is affine invariant.

### Bézier versus B-spline

- A degree-n Bézier uses `n+1` controls and generally has global control: moving one control influences the full curve.
- A B-spline uses basis functions over a knot vector; each control affects only a limited parameter interval (**local control**).
- Knot multiplicity reduces continuity. For degree `p`, a knot of multiplicity `m` has typically `C^(p-m)` continuity (when meaningful).
- A clamped knot vector makes the curve interpolate endpoints.

### NURBS

Non-Uniform Rational B-Spline:

$$
C(u)=\frac{\sum_i N_{i,p}(u)w_iP_i}
{\sum_iN_{i,p}(u)w_i}.
$$

Weights give extra shape control, and rational form can represent exact conic sections such as circles. “Non-uniform” refers to knot spacing/multiplicity; “rational” refers to weighted homogeneous division.

---

# Part X — fractals and recursive geometry

## 57. What is a fractal? **[ARK 264–268]**

A fractal is a shape with detailed structure at arbitrarily small scales, commonly generated by a simple recursive/iterative rule and often having fractal dimension larger than its topological dimension.

Typical properties:

- exact or statistical self-similarity/scale invariance;
- continuing detail under magnification;
- simple generative rule but high apparent complexity;
- noninteger or otherwise unusual dimension.

Finite computer images are approximations at a chosen recursion depth, not truly infinite structures.

## 58. Sierpiński triangle **[ARK 269–282]**

Construction: begin with an equilateral triangle; connect side midpoints, remove the central triangle, and repeat on each of the three remaining triangles.

At iteration `n`:

- number of retained triangles: `3^n`;
- side length of each: `a/2^n`;
- retained area:

$$
A_n=A_0\left(\frac34\right)^n\to0.
$$

The slide’s boundary accounting gives a perimeter growing as

$$
P_n=P_0\left(\frac32\right)^n\to\infty.
$$

Thus the limiting set can have zero area and unbounded total boundary length while living in the plane.

Recursive drawing:

```python
def sierpinski(a, b, c, depth, emit_triangle):
    if depth == 0:
        emit_triangle(a, b, c)
        return
    ab = (a + b) * 0.5
    bc = (b + c) * 0.5
    ca = (c + a) * 0.5
    sierpinski(a,  ab, ca, depth-1, emit_triangle)
    sierpinski(ab, b,  bc, depth-1, emit_triangle)
    sierpinski(ca, bc, c,  depth-1, emit_triangle)
```

Time/output size is `Theta(3^depth)` and recursion stack depth is `O(depth)`.

## 59. Koch curve **[ARK 283–292]**

Replace every segment by four segments, each one third as long, forming an outward equilateral bump.

At iteration `n`:

$$
segments=4^n,\qquad segmentLength=a/3^n,
$$

$$
L_n=a\left(\frac43\right)^n\to\infty.
$$

It remains spatially bounded but has infinite limiting length. A Koch snowflake made from three such sides has infinite perimeter but finite area.

## 60. Self-similarity and box-counting dimension **[ARK 293–305]**

If a shape consists of `N` self-similar copies, each scaled by linear factor `r<1`, then

$$
N=(1/r)^D,\qquad
\boxed{D=\frac{\log N}{\log(1/r)}}.
$$

Examples:

- line: `N=2,r=1/2 -> D=1`;
- square: `N=4,r=1/2 -> D=2`;
- cube: `N=8,r=1/2 -> D=3`;
- Sierpiński: `D=log 3/log 2≈1.585`;
- Koch: `D=log 4/log 3≈1.262`.

For more general sets, box-counting dimension is

$$
D=\lim_{\epsilon\to0}
\frac{\log N(\epsilon)}{\log(1/\epsilon)},
$$

where `N(epsilon)` is the number of size-epsilon boxes needed to cover the set. Real finite data gives an estimated slope over a scale range, not an exact infinite-limit dimension.

The slides give illustrative estimates for natural shapes such as coastline, clouds, lightning, and lung branching. These are scale- and measurement-dependent empirical characterizations, not exact self-similar dimensions.

## 61. Dragon and Hilbert curves **[ARK 306–329]**

### Dragon curve

Repeatedly fold/replace the curve with two perpendicular scaled copies. It has `N=2`, `r=1/sqrt(2)`, so

$$
D=\frac{\log2}{\log\sqrt2}=2.
$$

### Hilbert curve

Begin with a U-shaped order-1 curve; recursively place, orient, and connect four half-scale copies. It has `N=4`, `r=1/2`, hence `D=2`.

In the limiting mathematical construction, a space-filling curve continuously maps a 1D parameter interval onto every point of a 2D region. Every finite recursion is still a polyline and does not literally cover every point. The locality-preserving mapping is useful for spatial indexing, cache layout, and multidimensional traversal.

## 62. L-systems **[ARK 330–344]**

A Lindenmayer system generates structures by **parallel string rewriting**.

Components:

- axiom: initial string;
- productions: replacement for each symbol;
- iteration count;
- interpretation: turtle-graphics actions.

Typical turtle commands (symbol conventions vary by system):

- `F` or `X`: move/draw forward;
- `+`: turn right by delta;
- `-`: turn left by delta;
- `[`: push position and heading;
- `]`: pop/restore position and heading.

The important rule is that every symbol in one generation is rewritten **simultaneously** from the old string. Sequential in-place rewriting produces a different grammar.

Slide examples:

- Koch: axiom `F`, rule `F -> F-F++F-F`, angle 60 degrees.
- Sierpiński-like grammar: axiom `F-G-G`, rules `F -> F-G+F+G-F`, `G -> GG`, angle 120 degrees.
- Branching tree: axiom `F`, rules resembling `F -> T[-F][+F]`, `T -> TT`, angle 30 degrees; brackets preserve branch state.

```python
from math import cos, sin, radians

def rewrite(axiom, rules, generations):
    s = axiom
    for _ in range(generations):
        s = ''.join(rules.get(ch, ch) for ch in s)
    return s

def turtle_segments(program, angle_deg, step=1.0):
    x = y = 0.0
    heading = 0.0
    stack = []
    segments = []
    turn = radians(angle_deg)
    for ch in program:
        if ch in ('F', 'G', 'T', 'X'):
            nx = x + step * cos(heading)
            ny = y + step * sin(heading)
            segments.append(((x,y),(nx,ny)))
            x,y = nx,ny
        elif ch == '+': heading -= turn
        elif ch == '-': heading += turn
        elif ch == '[': stack.append((x,y,heading))
        elif ch == ']':
            if not stack: raise ValueError('unmatched ]')
            x,y,heading = stack.pop()
    if stack: raise ValueError('unmatched [')
    return segments

koch = rewrite('F', {'F':'F-F++F-F'}, 3)
segments = turtle_segments(koch, 60)
```

If the largest production expansion factor is `b`, generated string size can be exponential, `O(b^n)`. Stack depth reflects nested brackets, not necessarily generation depth. L-systems model plant branching and other natural recursive structure.

---

# Part XI — animation essentials

The decks mention animation applications, vertex deformation, camera paths, double buffering, and frame timing. This section supplies the viva-critical mechanism behind them.

## 63. Frames, state, and the animation loop

Animation displays changing scene states over time:

```text
while running:
    measure delta time
    read input
    update simulation/animation state
    render current state into back buffer
    present/swap
```

Movement should generally depend on elapsed time, not “units per frame,” or speed changes with FPS. A fixed simulation timestep gives deterministic/stable physics; rendering may interpolate between simulation states.

## 64. Keyframes and interpolation

A keyframe specifies values at selected times. Between scalar/vector keys `(t0,p0)` and `(t1,p1)`:

$$
u=\operatorname{clamp}\left(\frac{t-t_0}{t_1-t_0},0,1\right),
\quad p(t)=(1-u)p_0+up_1.
$$

Ease functions remap u to alter velocity. Smoothstep `3u²-2u³` has zero endpoint first derivatives. Cubic Hermite interpolation includes endpoint positions and tangents:

$$
p(u)=h_{00}p_0+h_{10}m_0+h_{01}p_1+h_{11}m_1.
$$

## 65. Rotation animation and quaternions

Euler angles are intuitive but order-dependent and can suffer **gimbal lock**. A unit quaternion represents rotation compactly without that singularity.

Normalized linear interpolation (nlerp) is cheap and adequate for small changes. Spherical interpolation (SLERP) follows constant angular speed on the unit 4D sphere:

$$
slerp(q_0,q_1,t)=
\frac{\sin((1-t)\Omega)}{\sin\Omega}q_0+
\frac{\sin(t\Omega)}{\sin\Omega}q_1.
$$

If `q0·q1<0`, negate one quaternion because `q` and `-q` represent the same rotation but one arc is shorter. For nearly identical quaternions, fall back to normalized LERP to avoid division by tiny `sin Omega`.

## 66. Skeletal animation

A skeleton is a hierarchy of bone transforms. A child’s world transform multiplies parent world transform by child local transform. Linear blend skinning uses weighted bone matrices:

$$
p'=\sum_j w_j M_j p,\qquad \sum_jw_j=1.
$$

Each `M_j` includes current bone pose and inverse bind pose. Normals/directions require appropriate linear/normal treatment. LBS is fast and GPU-friendly but can collapse volume (“candy-wrapper” artifact); dual-quaternion skinning improves rigid blending.

---

# Part XII — high-yield whiteboard explanations and viva traps

## 67. One-minute graphics-pipeline answer

“The application sends indexed vertices with attributes. A vertex shader converts model coordinates through model, view, and projection matrices into clip space. Hardware clips primitives before dividing by w, maps NDC to screen space, rasterizes triangles into fragments, and perspective-correctly interpolates attributes. A fragment shader computes colors using textures and lighting. Scissor, stencil, depth, and blending decide what reaches the color/depth/stencil framebuffer, which is then presented.”

## 68. One-minute rasterization versus ray tracing answer

“Rasterization asks which screen samples are covered by projected primitives, so it exploits coherent triangles and GPU parallelism for real time. Ray tracing asks what the nearest object is along each camera ray and naturally adds shadow/reflection/refraction rays. Rasterization usually approximates global effects; path tracing samples the rendering equation and can be physically accurate but needs many rays and acceleration structures.”

## 69. Whiteboard: transformation order

Draw a point `(1,1)`, scale it by 2 to `(2,2)`, then translate `(3,1)` to `(5,3)`. Write `p'=TSp`. Reverse it: translate first `(4,2)`, scale to `(8,4)`, write `p'=STp`. Conclude: matrix multiplication is associative, not commutative; with column vectors, rightmost acts first.

## 70. Whiteboard: z-buffer

Draw two overlapping triangles labeled A z=0.2 and B z=0.7. Under the standard `[0,1]` depth mapping with a `LESS` test, initialize every z-buffer entry to the farthest representable depth, usually `1.0`. Draw B, storing 0.7. Draw A; where they overlap, `0.2<0.7`, so replace color and depth. State that color and depth are separate buffers and that depth must be interpolated at each covered sample. Reversed-Z deliberately uses the opposite clear value/comparison convention, so never mix the two.

## 71. Whiteboard: barycentric coordinates

Draw triangle ABC and point P. Write `P=alpha A+beta B+gamma C`, `alpha+beta+gamma=1`. Explain weights as opposite-subtriangle area ratios. Nonnegative weights mean inside. Then say the same weights interpolate UV, color, normal, and depth; after projection, general attributes need division-by-w correction.

## 72. Whiteboard: ray-sphere

Write sphere `(P-C)·(P-C)=r²` and ray `P=O+td`. Substitute, collect quadratic coefficients, interpret discriminant, choose nearest valid positive root, and mention the second root is needed when the ray starts inside.

## 73. Whiteboard: Phong

Draw N, L, V, and reflected R. Explain:

```text
ambient: constant approximation of indirect light
diffuse: kd Il max(0,N·L), view independent
specular: ks Il max(0,R·V)^n, view dependent
```

Higher n means smaller/sharper highlight. State all direction vectors must be normalized and in the same coordinate space.

## 74. Compact comparison table

| Pair | Core distinction |
|---|---|
| Pixel vs fragment | storage/display element vs candidate contribution |
| Clipping vs culling | trim against boundary vs discard whole primitive |
| Model vs view matrix | object-local -> world vs world -> camera |
| Perspective vs orthographic | finite COP/foreshortening vs parallel rays/no depth-size change |
| Gouraud vs Phong shading | interpolate vertex lighting vs interpolate normals then light per fragment |
| Phong vs Blinn–Phong | reflection vector `R·V` vs halfway vector `N·H` |
| Ray casting vs ray tracing | primary rays only vs secondary rays/effects |
| Texture vs material | sampled data field vs full surface-response parameters/model |
| Albedo vs final color | intrinsic reflected base fraction vs result after lighting |
| Normal map vs displacement | changes shading normal vs moves geometry |
| DDA vs Bresenham | floating increments vs integer decision recurrence |
| Affine vs projective | preserves parallelism vs only collinearity generally |
| Bézier vs B-spline | global polynomial control vs knot-based local control |
| Double buffering vs VSync | complete off-screen frames vs synchronize presentation to refresh |

## 75. Frequent viva traps—say these correctly

1. **A fragment is not automatically a pixel.** It must survive tests and may blend.
2. **The nearest-depth inequality is a convention.** Standard and reversed-z pipelines differ.
3. **Matrix order depends on vector convention.** State column versus row vectors.
4. **Perspective divide is by homogeneous w, not “always by z.”** In one simple matrix `w=z`; standard OpenGL commonly produces `w=-z_eye`.
5. **Clip before perspective divide.** Otherwise near/eye crossings are unstable.
6. **Normals use inverse-transpose under general affine transforms.**
7. **Interpolated normals need renormalization.**
8. **Back-face sign is convention-dependent.** Winding, handedness, and direction definition matter.
9. **Uniform t is not necessarily uniform speed along a curve.**
10. **A degree-n Bézier has n+1 controls.** It generally does not pass through interior controls.
11. **Barycentric coordinates sum to one.** Nonnegative weights indicate the triangle’s convex hull.
12. **Bilinear means four texels; trilinear means two bilinear mip levels.**
13. **MSAA mainly addresses geometric coverage edges.** It does not automatically cure shader/texture aliasing.
14. **Ambient is not physically correct global illumination.**
15. **Specular is view-dependent; Lambert diffuse is view-independent.**
16. **Ray direction normalization affects whether t is distance.**
17. **Sphere’s second root matters for an origin inside the sphere.**
18. **A BVH is not guaranteed O(log N).** Worst case can be linear.
19. **Path tracing can be unbiased and still noisy.**
20. **Epsilon is necessary but scale-sensitive.**
21. **Transparent rendering is order-dependent under ordinary alpha blending.**
22. **Gamma-encoded colors should not be treated as linear light.**
23. **L-system rules update simultaneously per generation.**
24. **Finite fractal drawings are approximations.** Infinite-limit properties do not literally hold at finite depth.
25. **Phong shading and Phong illumination are different concepts.**

## 76. Rapid-fire questions with complete short answers

### What is computer graphics?

The use of computation to synthesize, transform, render, and manipulate visual information.

### Why use homogeneous coordinates?

They make translation, affine transforms, and projective perspective division expressible in one composable matrix framework; directions use w=0 and points usually w=1.

### Why triangles?

Three noncollinear points always define a plane; triangles are convex, have simple inside tests/interpolation, tessellate arbitrary surfaces, and map efficiently to hardware.

### Why is rasterization faster than ray tracing?

It exploits projected primitive coherence, massive parallelism, fixed-function hardware, and local approximations instead of searching the scene and recursively sampling global light paths per ray.

### Why is a z-buffer useful?

It resolves nearest opaque visibility per sample with simple constant-time comparisons, independent of draw order except ties/precision.

### What does the projection matrix do?

It maps camera-space coordinates to homogeneous clip space, encoding the frustum; clipping and division by w then produce canonical NDC.

### Why do distant perspective objects look smaller?

Similar triangles give projected size proportional to focal distance divided by object depth.

### Why clamp `N·L`?

A negative dot means the light lies below the oriented surface; negative radiance is meaningless in this local model.

### What is attenuation?

The reduction of received light with distance; an ideal point source follows inverse square because fixed power spreads over area proportional to distance squared.

### What is a texture?

A sampled function over surface coordinates that supplies color or another material/geometric property.

### Why mipmaps?

They prefilter textures at multiple resolutions so minified footprints average many texels instead of aliasing.

### What is the convex-hull property of Bézier curves?

Every curve point is a nonnegative Bernstein-weighted average whose weights sum to one, so it cannot leave the control-point convex hull.

### What is fractal dimension?

A scaling exponent measuring how required detail count grows as measurement scale shrinks; self-similar dimension is `log N/log(1/r)`.

## 77. Algorithm audit table: invariant, cost, and failure mode

| Algorithm | Correctness invariant / central test | Time | Working space | Edge case to say aloud |
|---|---|---:|---:|---|
| DDA line | advance one major-axis step while continuous `(x,y)` remains on ideal parametric line | `O(max(|dx|,|dy|))` | `O(1)` excluding output | coincident endpoints; floating rounding drift |
| Bresenham line | integer error tracks which adjacent raster point is closer to ideal line | `O(max(|dx|,|dy|))` | `O(1)` | all octants, steep/negative/vertical lines |
| Midpoint circle | implicit circle sign at midpoint selects E versus SE; eightfold symmetry | `O(r)` | `O(1)` | radius 0 and duplicate symmetric writes |
| Scanline polygon fill | sorted crossings toggle inside/outside; AET contains exactly edges crossing current y | `O(P + edge maintenance)` | `O(E)` | lower-inclusive/upper-exclusive vertex rule |
| Triangle rasterization | three oriented edge signs agree for covered sample | `O(bounding-box samples)` | `O(1)` per triangle | degenerate area; consistent top-left tie rule |
| Cohen–Sutherland | outcode OR=0 accepts; AND!=0 rejects; otherwise clip one outside endpoint | constant bounded iterations in 2D | `O(1)` | horizontal/vertical division |
| Liang–Barsky | `[t_enter,t_leave]` is intersection of all half-space parameter intervals | `O(number of boundaries)` | `O(1)` | parallel outside inequality |
| Sutherland–Hodgman | after each pass, current polygon satisfies every processed half-space | `O(nk + output)` | `O(output)` | partial triangle may need retriangulation |
| Z-buffer | stored depth/color is nearest accepted fragment seen so far at each sample | `O(total fragments)` | `O(WH*samples)` | equal depth, precision, transparency |
| Ray primitive hit | return smallest valid t in current `[t_min,t_max]` | `O(1)` per analytic primitive | `O(1)` | near-parallel/tangent/inside cases |
| BVH traversal | skipped node cannot contain a hit closer than current best | expected sublinear; worst `O(N)` | `O(tree depth)` | overlapping bounds / unbalanced tree |
| De Casteljau | each level is a convex interpolation of the preceding control polygon | `O(n²)` | `O(n)` | valid extrapolation outside `[0,1]`, but convex-hull guarantee is then lost |
| L-system rewriting | generation `g+1` is produced simultaneously from immutable generation `g` | often exponential in depth/output | `O(output)` | unmatched state brackets; explosive string size |

---

# Part XIII — source-page coverage matrix

Every physical page belongs to exactly one row below, including cover, section-divider, example-image, question, and reference pages. Counts are inclusive: `end-start+1`.

## ARK_merged.pdf — exact 473-page partition

| Physical PDF pages | Count | Slide block reconstructed here |
|---:|---:|---|
| 1–31 | 31 | motivation, physical light story, reverse ray casting, one ray per pixel |
| 32–93 | 62 | ray math; plane/triangle/barycentric/sphere/quadric/AABB intersections |
| 94–130 | 37 | pinhole, virtual image plane, orthographic camera, camera basis and pixel-ray formula |
| 131–145 | 15 | ray casting vs tracing, secondary rays, recursion, shadows, reflections, epsilon |
| 146–152 | 7 | complexity, naive traversal, BVH, ray-tracing hardware |
| 153–158 | 6 | path tracing, rendering equation, comparison and references |
| 159–168 | 10 | lighting motivation and physical-to-code challenge |
| 169–206 | 38 | natural light, point/directional/spot/ambient light and attenuation |
| 207–213 | 7 | normals for triangles, spheres, planes, implicit surfaces |
| 214–250 | 37 | Phong ambient/diffuse/specular, reflection, shininess, Blinn–Phong |
| 251–263 | 13 | UVs, mappings, texture sampling/filtering, texture kinds, TBN normal mapping |
| 264–305 | 42 | fractal definition, Sierpiński, Koch, dimension and natural examples |
| 306–329 | 24 | Dragon, Hilbert, and space-filling curves |
| 330–346 | 17 | L-systems, grammars, branching/natural structures, questions/references |
| 347–363 | 17 | rasterization motivation, real-time constraint, approximations |
| 364–371 | 8 | GPU history, CPU/GPU comparison, modern GPU roles |
| 372–393 | 22 | graphics-pipeline overview, data flow, programmable/fixed stages |
| 394–402 | 9 | APIs, shading languages, GLSL types/qualifiers/examples |
| 403–417 | 15 | input assembly, attributes/topology/indexing, vertex shader, spaces, Gouraud |
| 418–424 | 7 | tessellation and geometry shaders, LOD, billboarding |
| 425–436 | 12 | primitive assembly, winding, clipping, Sutherland–Hodgman, culling |
| 437–444 | 8 | triangle rasterization, edge functions, barycentrics, interpolation, fragments |
| 445–457 | 13 | fragment shading, Phong/Gouraud, GLSL lighting and multitexture examples |
| 458–465 | 8 | per-fragment tests, early-z, blending, stencil/scissor |
| 466–473 | 8 | framebuffer, attachments, double buffering, VSync, summary/references |
| **Total** | **473** | **No gap and no overlap** |

Arithmetic check:

```text
31+62+37+15+7+6+10+38+7+37+13+42+24+17+17+8+22+9+15+7+12+8+13+8+8 = 473
```

## IJ_merged2.pdf — exact 263-page partition

| Physical PDF pages | Count | Slide block reconstructed here |
|---:|---:|---|
| 1–36 | 36 | introduction/history/applications; modeling/view/lighting/projection/raster/texture/ray overview |
| 37–72 | 36 | points/vectors, dot/cross, projection/reflection, lines, planes, intersections |
| 73–84 | 12 | transformation motivation and Euclidean/similarity/linear/affine/projective taxonomy |
| 85–107 | 23 | homogeneous coordinates; translation/scale/rotation/reflection/shear/inverses |
| 108–137 | 30 | composition order, pivot/line transforms, arbitrary-axis alignment, Rodrigues, axis extraction |
| 138–156 | 19 | projection terminology/taxonomy, perspective anomalies and vanishing points |
| 157–170 | 14 | perspective derivation/matrix, generalized projection, OpenGL setup code |
| 171–190 | 20 | pipeline revisit, camera position, LookAt/view matrix, OpenGL projection views |
| 191–198 | 8 | orthographic/axonometric/isometric/oblique/Cavalier/Cabinet projection |
| 199–224 | 26 | z-buffer example, scanline depth finding, clipping and pseudocode |
| 225–263 | 39 | parametric/Bézier curves, continuity, Bernstein/convex hull, matrix/code, references |
| **Total** | **263** | **No gap and no overlap** |

Arithmetic check:

```text
36+36+12+23+30+19+14+20+8+26+39 = 263
```

## Grand coverage check

```text
ARK_merged.pdf     473 pages
IJ_merged2.pdf     263 pages
                   ---------
Audited total      736 pages
```

---

# Final recall sheet — formulas to be able to write without prompting

```text
Ray:                   P(t)=O+td
Plane:                 n·P+D=0
Ray-plane:             t=-(n·O+D)/(n·d)
Barycentric:           P=alpha*A+beta*B+gamma*C; sum=1
Sphere:                (P-C)·(P-C)=r²
Quadratic roots:       t=(-b±sqrt(b²-4ac))/(2a)
AABB:                  enter=max(axis minima), exit=min(axis maxima)
Reflection:            R=I-2(I·N)N
Lambert:               kd*Il*max(0,N·L)
Phong specular:        ks*Il*max(0,R·V)^n
Blinn halfway:         H=normalize(L+V)
Point attenuation:     approximately 1/d²
Model/clip chain:      p_clip=P*V*M*p_model
Perspective divide:    p_ndc=p_clip.xyz/p_clip.w
Viewport x:            x0+(x_ndc+1)W/2
Normal matrix:         transpose(inverse(mat3(M)))
LERP:                  (1-t)A+tB
Quadratic Bézier:      (1-t)²P0+2t(1-t)P1+t²P2
Cubic Bézier:          (1-t)³P0+3t(1-t)²P1+3t²(1-t)P2+t³P3
Fractal dimension:     log(N)/log(1/r)
Alpha over:            C=alpha*Cs+(1-alpha)*Cd
Perspective attribute: sum(lambda*a/w)/sum(lambda/w)
Rendering equation:    outgoing = emitted + hemisphere integral
```

Before the viva, practice deriving at least these on a blank board: transform order, LookAt matrix, simple perspective by similar triangles, ray-plane, ray-sphere, barycentric inside test, Bresenham decision idea, z-buffer, Phong components, Bézier from LERPs, and self-similar dimension.
