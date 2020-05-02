# Ray-Tracing
Ray tracing is a rendering technique for generating an image by tracing the path of light as pixels in an image plane. Basically, to generate an image of the environment you use view rays to calculate the color of each pixel. I have used several algebraic approaches to calculate ray-sphere and ray-plane intersections.

![Ray-tracing-gif](https://www.scratchapixel.com/images/upload/ray-tracing-camera/campixel.gif)

### Shading
Another problem to solve was calculating if the point is under a shadow or not. To check it, you need to generate a **shadow ray** to check if there are obstacles between the light source and the intersection point. 
![Ray-tracing-gif-2](https://www.scratchapixel.com/images/upload/introduction-to-ray-tracing/lightingnoshadow.gif)
![Ray-tracing-gif-3](https://www.scratchapixel.com/images/upload/introduction-to-ray-tracing/lightingshadow.gif)


However, without a proper shading model results look pretty unrealistic. For example the image below consists of 2 spheres aligned one after another on light source's direction. 

![A-bad-example](https://github.com/safakozdek/Ray-Tracing/blob/master/some%20results/image_without_phong_shading.jpg)


### Phong Model
To make it more realistic, I decided to use [Phong Reflection Model](https://en.wikipedia.org/wiki/Phong_reflection_model) without specular light. By the help of ambient and diffuse terms it became easier to generate a more realistic image.
![Phong-Model](https://github.com/safakozdek/Ray-Tracing/blob/master/some%20results/Phong_components_version_4_wikipedia.png)



Also I used a recursive ray tracing approach to add reflections:

![Recursive-diffuse-color](https://www.scratchapixel.com/images/upload/ray-tracing-refresher/rt-reflection2.gif)


### Results
The final results looks more realistic: 
![Result](https://github.com/safakozdek/Ray-Tracing/blob/master/some%20results/output1.png)

## How to run?

### Input.txt format:
**[Number of spheres]** \
*For each sphere:*
* **[colorR, colorG, colorB]** → Comma seperated RGB values 
* **[centerX, centerY, centerZ]** → Comma seperated center coordinates 
* **[radius]** 
* **[diffuse Coefficient]** 
* **[reflection Coefficient]** 

**[Number of planes]**\
*For each plane:*
* **[colorR, colorG, colorB]** → Comma seperated RGB values
* **[centerX, centerY, centerZ]** → Comma seperated point coordinates 
* **[normalX, normalY, normalZ]** → Comma seperated normal vector 
* **[diffuse Coefficient]**
* **[reflection Coefficient]** 


You can check example [input.txt](https://github.com/safakozdek/Ray-Tracing/blob/master/input.txt)
### Run:
You need an environment that has python3 with numpy and pillow libraries installed. Then follow the steps:
* Modify input.txt which is located in the same directory with ray_tracer.py
* Use `python ray_tracer.py` to run the script. 
* Output.png or output.jpeg will be generated.

PS: It takes a few minutes to generate the output. Please be patient.
