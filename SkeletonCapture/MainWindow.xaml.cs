//------------------------------------------------------------------------------
// <copyright file="MainWindow.xaml.cs" company="Microsoft">
//     Copyright (c) Microsoft Corporation.  All rights reserved.
// </copyright>
//------------------------------------------------------------------------------

namespace Microsoft.Samples.Kinect.SkeletonBasics
{
    using System.IO;
    using System.Windows;
    using System.Windows.Media;
    using Microsoft.Kinect;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // Name of the movement captured
        private String nameFile = "name";
        // Name of the path where files will be saved
        private String path = @"C:\Users\";
        /// <summary>
        /// Width of output drawing
        /// </summary>
        private const float RenderWidth = 640.0f;

        /// <summary>
        /// Height of our output drawing
        /// </summary>
        private const float RenderHeight = 480.0f;

        /// <summary>
        /// Thickness of drawn joint lines
        /// </summary>
        private const double JointThickness = 3;

        /// <summary>
        /// Thickness of body center ellipse
        /// </summary>
        private const double BodyCenterThickness = 10;

        /// <summary>
        /// Thickness of clip edge rectangles
        /// </summary>
        private const double ClipBoundsThickness = 10;

        /// <summary>
        /// Brush used to draw skeleton center point
        /// </summary>
        private readonly Brush centerPointBrush = Brushes.Blue;

        /// <summary>
        /// Brush used for drawing joints that are currently tracked
        /// </summary>
        private readonly Brush trackedJointBrush = new SolidColorBrush(Color.FromArgb(255, 68, 192, 68));

        /// <summary>
        /// Brush used for drawing joints that are currently inferred
        /// </summary>        
        private readonly Brush inferredJointBrush = Brushes.Yellow;

        /// <summary>
        /// Pen used for drawing bones that are currently tracked
        /// </summary>
        private readonly Pen trackedBonePen = new Pen(Brushes.Green, 6);

        /// <summary>
        /// Pen used for drawing bones that are currently inferred
        /// </summary>        
        private readonly Pen inferredBonePen = new Pen(Brushes.Gray, 1);

        /// <summary>
        /// Active Kinect sensor
        /// </summary>
        private KinectSensor sensor;

        /// <summary>
        /// Drawing group for skeleton rendering output
        /// </summary>
        private DrawingGroup drawingGroup;

        /// <summary>
        /// Drawing image that we will display
        /// </summary>
        private DrawingImage imageSource;

        // tab of skeleton's joints (for each time t)
        private double[,] matJoints = new double[20, 4];// 20 different joints and 4 dimensions : x y z and w
        // Creation of the list where all matJoints will be stored
        private IList<double[,]> listMatJoints = new List<double[,]>();
        // Mouvment counter
        private int j=0;
        // We create a StreamWritter to write in a file
        private StreamWriter sw;

        /// <summary>
        /// Initializes a new instance of the MainWindow class.
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Draws indicators to show which edges are clipping skeleton data
        /// </summary>
        /// <param name="skeleton">skeleton to draw clipping information for</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        private static void RenderClippedEdges(Skeleton skeleton, DrawingContext drawingContext)
        {
            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Bottom))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, RenderHeight - ClipBoundsThickness, RenderWidth, ClipBoundsThickness));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Top))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, RenderWidth, ClipBoundsThickness));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Left))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, ClipBoundsThickness, RenderHeight));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Right))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(RenderWidth - ClipBoundsThickness, 0, ClipBoundsThickness, RenderHeight));
            }
        }

        /// <summary>
        /// Execute startup tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void WindowLoaded(object sender, RoutedEventArgs e)
        {
            if (System.IO.File.Exists(path + nameFile + ".txt"))
            {
                try
                {
                    System.IO.File.Delete(path + nameFile + ".txt");
                }
                catch (System.IO.IOException e2)
                {
                    Console.WriteLine(e2.Message);
                    return;
                }
            }

            sw = new StreamWriter(path + nameFile + ".txt", true, System.Text.Encoding.ASCII);

            // Create the drawing group we'll use for drawing
            this.drawingGroup = new DrawingGroup();

            // Create an image source that we can use in our image control
            this.imageSource = new DrawingImage(this.drawingGroup);

            // Display the drawing using our image control
            Image.Source = this.imageSource;

            // Look through all sensors and start the first connected one.
            // This requires that a Kinect is connected at the time of app startup.
            // To make your app robust against plug/unplug, 
            // it is recommended to use KinectSensorChooser provided in Microsoft.Kinect.Toolkit (See components in Toolkit Browser).
            foreach (var potentialSensor in KinectSensor.KinectSensors)
            {
                if (potentialSensor.Status == KinectStatus.Connected)
                {
                    this.sensor = potentialSensor;
                    break;
                }
            }

            if (null != this.sensor)
            {
                // Turn on the skeleton stream to receive skeleton frames
                this.sensor.SkeletonStream.Enable();

                // Add an event handler to be called whenever there is new color frame data
                this.sensor.SkeletonFrameReady += this.SensorSkeletonFrameReady;

                // Start the sensor!
                try
                {
                    this.sensor.Start();
                }
                catch (IOException)
                {
                    this.sensor = null;
                }
            }

            if (null == this.sensor)
            {
                this.statusBarText.Text = Properties.Resources.NoKinectReady;
            }
        }

        /// <summary>
        /// Execute shutdown tasks
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void WindowClosing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            sw.Close();
            if (null != this.sensor)
            {
                this.sensor.Stop();
            }
        }

        /// <summary>
        /// Event handler for Kinect sensor's SkeletonFrameReady event
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void SensorSkeletonFrameReady(object sender, SkeletonFrameReadyEventArgs e)
        {
            Skeleton[] skeletons = new Skeleton[0];

            using (SkeletonFrame skeletonFrame = e.OpenSkeletonFrame())
            {
                if (skeletonFrame != null)
                {
                    skeletons = new Skeleton[skeletonFrame.SkeletonArrayLength];
                    skeletonFrame.CopySkeletonDataTo(skeletons);
                }
            }

            using (DrawingContext dc = this.drawingGroup.Open())
            {
                // Draw a transparent background to set the render size
                dc.DrawRectangle(Brushes.Black, null, new Rect(0.0, 0.0, RenderWidth, RenderHeight));
                if (skeletons.Length != 0)
                {
                    foreach (Skeleton skel in skeletons)
                    {
                        RenderClippedEdges(skel, dc);
                        if (skel.TrackingState == SkeletonTrackingState.Tracked)
                        {
                            //Console.WriteLine("position x = " + skel.Position.X);
                            this.DrawBonesAndJoints(skel, dc);
                        }
                        else if (skel.TrackingState == SkeletonTrackingState.PositionOnly)
                        {
                            //Console.WriteLine("position x = " + skel.Position.X);
                            dc.DrawEllipse(
                            this.centerPointBrush,
                            null,
                            this.SkeletonPointToScreen(skel.Position),
                            BodyCenterThickness,
                            BodyCenterThickness);
                        }
                    }
                }

                // prevent drawing outside of our render area
                this.drawingGroup.ClipGeometry = new RectangleGeometry(new Rect(0.0, 0.0, RenderWidth, RenderHeight));
            }
        }

        /// <summary>
        /// Draws a skeleton's bones and joints
        /// </summary>
        /// <param name="skeleton">skeleton to draw</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        private void DrawBonesAndJoints(Skeleton skeleton, DrawingContext drawingContext)
        {
            // Render Torso
            this.DrawBone(skeleton, drawingContext, JointType.Head, JointType.ShoulderCenter);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.ShoulderLeft);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.ShoulderRight);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.Spine);
            this.DrawBone(skeleton, drawingContext, JointType.Spine, JointType.HipCenter);
            this.DrawBone(skeleton, drawingContext, JointType.HipCenter, JointType.HipLeft);
            this.DrawBone(skeleton, drawingContext, JointType.HipCenter, JointType.HipRight);

            // Left Arm
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderLeft, JointType.ElbowLeft);
            this.DrawBone(skeleton, drawingContext, JointType.ElbowLeft, JointType.WristLeft);
            this.DrawBone(skeleton, drawingContext, JointType.WristLeft, JointType.HandLeft);

            // Right Arm
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderRight, JointType.ElbowRight);
            this.DrawBone(skeleton, drawingContext, JointType.ElbowRight, JointType.WristRight);
            this.DrawBone(skeleton, drawingContext, JointType.WristRight, JointType.HandRight);

            // Left Leg
            this.DrawBone(skeleton, drawingContext, JointType.HipLeft, JointType.KneeLeft);
            this.DrawBone(skeleton, drawingContext, JointType.KneeLeft, JointType.AnkleLeft);
            this.DrawBone(skeleton, drawingContext, JointType.AnkleLeft, JointType.FootLeft);

            // Right Leg
            this.DrawBone(skeleton, drawingContext, JointType.HipRight, JointType.KneeRight);
            this.DrawBone(skeleton, drawingContext, JointType.KneeRight, JointType.AnkleRight);
            this.DrawBone(skeleton, drawingContext, JointType.AnkleRight, JointType.FootRight);


            // Render Joints
            foreach (Joint joint in skeleton.Joints)
            {
                Brush drawBrush = null;

                if (joint.TrackingState == JointTrackingState.Tracked)
                {
                    switch (joint.JointType)
                    {
                        case JointType.HipCenter:
                            matJoints[0, 0] = joint.Position.X;
                            matJoints[0, 1] = joint.Position.Y;
                            matJoints[0, 2] = joint.Position.Z;
                            matJoints[0, 3] = 1;
                            break;
                        case JointType.Spine:
                            matJoints[1, 0] = joint.Position.X;
                            matJoints[1, 1] = joint.Position.Y;
                            matJoints[1, 2] = joint.Position.Z;
                            matJoints[1, 3] = 1;
                            break;
                        case JointType.ShoulderCenter:
                            matJoints[2, 0] = joint.Position.X;
                            matJoints[2, 1] = joint.Position.Y;
                            matJoints[2, 2] = joint.Position.Z;
                            matJoints[2, 3] = 1;
                            break;
                        case JointType.Head:
                            matJoints[3, 0] = joint.Position.X;
                            matJoints[3, 1] = joint.Position.Y;
                            matJoints[3, 2] = joint.Position.Z;
                            matJoints[3, 3] = 1;
                            break;
                        case JointType.ShoulderLeft:
                            matJoints[4, 0] = joint.Position.X;
                            matJoints[4, 1] = joint.Position.Y;
                            matJoints[4, 2] = joint.Position.Z;
                            matJoints[4, 3] = 1;
                            break;
                        case JointType.ElbowLeft:
                            matJoints[5, 0] = joint.Position.X;
                            matJoints[5, 1] = joint.Position.Y;
                            matJoints[5, 2] = joint.Position.Z;
                            matJoints[5, 3] = 1;
                            break;
                        case JointType.WristLeft:
                            matJoints[6, 0] = joint.Position.X;
                            matJoints[6, 1] = joint.Position.Y;
                            matJoints[6, 2] = joint.Position.Z;
                            matJoints[6, 3] = 1;
                            break;
                        case JointType.HandLeft:
                            matJoints[7, 0] = joint.Position.X;
                            matJoints[7, 1] = joint.Position.Y;
                            matJoints[7, 2] = joint.Position.Z;
                            matJoints[7, 3] = 1;
                            break;
                        case JointType.ShoulderRight:
                            matJoints[8, 0] = joint.Position.X;
                            matJoints[8, 1] = joint.Position.Y;
                            matJoints[8, 2] = joint.Position.Z;
                            matJoints[8, 3] = 1;
                            break;
                        case JointType.ElbowRight:
                            matJoints[9, 0] = joint.Position.X;
                            matJoints[9, 1] = joint.Position.Y;
                            matJoints[9, 2] = joint.Position.Z;
                            matJoints[9, 3] = 1;
                            break;
                        case JointType.WristRight:
                            matJoints[10, 0] = joint.Position.X;
                            matJoints[10, 1] = joint.Position.Y;
                            matJoints[10, 2] = joint.Position.Z;
                            matJoints[10, 3] = 1;
                            break;
                        case JointType.HandRight:
                            matJoints[11, 0] = joint.Position.X;
                            matJoints[11, 1] = joint.Position.Y;
                            matJoints[11, 2] = joint.Position.Z;
                            matJoints[11, 3] = 1;
                            break;
                        case JointType.HipLeft:
                            matJoints[12, 0] = joint.Position.X;
                            matJoints[12, 1] = joint.Position.Y;
                            matJoints[12, 2] = joint.Position.Z;
                            matJoints[12, 3] = 1;
                            break;
                        case JointType.KneeLeft:
                            matJoints[13, 0] = joint.Position.X;
                            matJoints[13, 1] = joint.Position.Y;
                            matJoints[13, 2] = joint.Position.Z;
                            matJoints[13, 3] = 1;
                            break;
                        case JointType.AnkleLeft:
                            matJoints[14, 0] = joint.Position.X;
                            matJoints[14, 1] = joint.Position.Y;
                            matJoints[14, 2] = joint.Position.Z;
                            matJoints[14, 3] = 1;
                            break;
                        case JointType.FootLeft:
                            matJoints[15, 0] = joint.Position.X;
                            matJoints[15, 1] = joint.Position.Y;
                            matJoints[15, 2] = joint.Position.Z;
                            matJoints[15, 3] = 1;
                            break;
                        case JointType.HipRight:
                            matJoints[16, 0] = joint.Position.X;
                            matJoints[16, 1] = joint.Position.Y;
                            matJoints[16, 2] = joint.Position.Z;
                            matJoints[16, 3] = 1;
                            break;
                        case JointType.KneeRight:
                            matJoints[17, 0] = joint.Position.X;
                            matJoints[17, 1] = joint.Position.Y;
                            matJoints[17, 2] = joint.Position.Z;
                            matJoints[17, 3] = 1;
                            break;
                        case JointType.AnkleRight:
                            matJoints[18, 0] = joint.Position.X;
                            matJoints[18, 1] = joint.Position.Y;
                            matJoints[18, 2] = joint.Position.Z;
                            matJoints[18, 3] = 1;
                            break;
                        case JointType.FootRight:
                            matJoints[19, 0] = joint.Position.X;
                            matJoints[19, 1] = joint.Position.Y;
                            matJoints[19, 2] = joint.Position.Z;
                            matJoints[19, 3] = 1;
                            break;
                    }
                    drawBrush = this.trackedJointBrush;
                }
                else if (joint.TrackingState == JointTrackingState.Inferred)
                {
                    switch (joint.JointType)
                    {
                        case JointType.HipCenter:
                            matJoints[0, 0] = joint.Position.X;
                            matJoints[0, 1] = joint.Position.Y;
                            matJoints[0, 2] = joint.Position.Z;
                            matJoints[0, 3] = 0;
                            break;
                        case JointType.Spine:
                            matJoints[1, 0] = joint.Position.X;
                            matJoints[1, 1] = joint.Position.Y;
                            matJoints[1, 2] = joint.Position.Z;
                            matJoints[1, 3] = 0;
                            break;
                        case JointType.ShoulderCenter:
                            matJoints[2, 0] = joint.Position.X;
                            matJoints[2, 1] = joint.Position.Y;
                            matJoints[2, 2] = joint.Position.Z;
                            matJoints[2, 3] = 0;
                            break;
                        case JointType.Head:
                            matJoints[3, 0] = joint.Position.X;
                            matJoints[3, 1] = joint.Position.Y;
                            matJoints[3, 2] = joint.Position.Z;
                            matJoints[3, 3] = 0;
                            break;
                        case JointType.ShoulderLeft:
                            matJoints[4, 0] = joint.Position.X;
                            matJoints[4, 1] = joint.Position.Y;
                            matJoints[4, 2] = joint.Position.Z;
                            matJoints[4, 3] = 0;
                            break;
                        case JointType.ElbowLeft:
                            matJoints[5, 0] = joint.Position.X;
                            matJoints[5, 1] = joint.Position.Y;
                            matJoints[5, 2] = joint.Position.Z;
                            matJoints[5, 3] = 0;
                            break;
                        case JointType.WristLeft:
                            matJoints[6, 0] = joint.Position.X;
                            matJoints[6, 1] = joint.Position.Y;
                            matJoints[6, 2] = joint.Position.Z;
                            matJoints[6, 3] = 0;
                            break;
                        case JointType.HandLeft:
                            matJoints[7, 0] = joint.Position.X;
                            matJoints[7, 1] = joint.Position.Y;
                            matJoints[7, 2] = joint.Position.Z;
                            matJoints[7, 3] = 0;
                            break;
                        case JointType.ShoulderRight:
                            matJoints[8, 0] = joint.Position.X;
                            matJoints[8, 1] = joint.Position.Y;
                            matJoints[8, 2] = joint.Position.Z;
                            matJoints[8, 3] = 0;
                            break;
                        case JointType.ElbowRight:
                            matJoints[9, 0] = joint.Position.X;
                            matJoints[9, 1] = joint.Position.Y;
                            matJoints[9, 2] = joint.Position.Z;
                            matJoints[9, 3] = 0;
                            break;
                        case JointType.WristRight:
                            matJoints[10, 0] = joint.Position.X;
                            matJoints[10, 1] = joint.Position.Y;
                            matJoints[10, 2] = joint.Position.Z;
                            matJoints[10, 3] = 0;
                            break;
                        case JointType.HandRight:
                            matJoints[11, 0] = joint.Position.X;
                            matJoints[11, 1] = joint.Position.Y;
                            matJoints[11, 2] = joint.Position.Z;
                            matJoints[11, 3] = 0;
                            break;
                        case JointType.HipLeft:
                            matJoints[12, 0] = joint.Position.X;
                            matJoints[12, 1] = joint.Position.Y;
                            matJoints[12, 2] = joint.Position.Z;
                            matJoints[12, 3] = 0;
                            break;
                        case JointType.KneeLeft:
                            matJoints[13, 0] = joint.Position.X;
                            matJoints[13, 1] = joint.Position.Y;
                            matJoints[13, 2] = joint.Position.Z;
                            matJoints[13, 3] = 0;
                            break;
                        case JointType.AnkleLeft:
                            matJoints[14, 0] = joint.Position.X;
                            matJoints[14, 1] = joint.Position.Y;
                            matJoints[14, 2] = joint.Position.Z;
                            matJoints[14, 3] = 0;
                            break;
                        case JointType.FootLeft:
                            matJoints[15, 0] = joint.Position.X;
                            matJoints[15, 1] = joint.Position.Y;
                            matJoints[15, 2] = joint.Position.Z;
                            matJoints[15, 3] = 0;
                            break;
                        case JointType.HipRight:
                            matJoints[16, 0] = joint.Position.X;
                            matJoints[16, 1] = joint.Position.Y;
                            matJoints[16, 2] = joint.Position.Z;
                            matJoints[16, 3] = 0;
                            break;
                        case JointType.KneeRight:
                            matJoints[17, 0] = joint.Position.X;
                            matJoints[17, 1] = joint.Position.Y;
                            matJoints[17, 2] = joint.Position.Z;
                            matJoints[17, 3] = 0;
                            break;
                        case JointType.AnkleRight:
                            matJoints[18, 0] = joint.Position.X;
                            matJoints[18, 1] = joint.Position.Y;
                            matJoints[18, 2] = joint.Position.Z;
                            matJoints[18, 3] = 0;
                            break;
                        case JointType.FootRight:
                            matJoints[19, 0] = joint.Position.X;
                            matJoints[19, 1] = joint.Position.Y;
                            matJoints[19, 2] = joint.Position.Z;
                            matJoints[19, 3] = 0;
                            break;
                    }
                    drawBrush = this.inferredJointBrush;
                }
                if (drawBrush != null)
                {
                    drawingContext.DrawEllipse(drawBrush, null, this.SkeletonPointToScreen(joint.Position), JointThickness, JointThickness);
                }
                
            }
            
            listMatJoints.Add(matJoints);

            try
            {
                sw.WriteLine(j + "\n");
            }
            catch (ObjectDisposedException e)
            {
                Console.WriteLine(e.ToString());
            }

            for (int i = 0; i < 20; i++)
            {
                try
                {
                    sw.WriteLine(listMatJoints.Last()[i, 0].ToString() + " " + listMatJoints.Last()[i, 1].ToString() + " " + listMatJoints.Last()[i, 2].ToString() + " " + listMatJoints.Last()[i, 3].ToString());
                }
                catch (ObjectDisposedException e2)
                {
                    Console.WriteLine(e2.ToString());
                }
            }
            j++;
        }


        /// <summary>
        /// Maps a SkeletonPoint to lie within our render space and converts to Point
        /// </summary>
        /// <param name="skelpoint">point to map</param>
        /// <returns>mapped point</returns>
        private Point SkeletonPointToScreen(SkeletonPoint skelpoint)
        {
            // Convert point to depth space.  
            // We are not using depth directly, but we do want the points in our 640x480 output resolution.
            DepthImagePoint depthPoint = this.sensor.CoordinateMapper.MapSkeletonPointToDepthPoint(skelpoint, DepthImageFormat.Resolution640x480Fps30);
            return new Point(depthPoint.X, depthPoint.Y);
        }

        /// <summary>
        /// Draws a bone line between two joints
        /// </summary>
        /// <param name="skeleton">skeleton to draw bones from</param>
        /// <param name="drawingContext">drawing context to draw to</param>
        /// <param name="jointType0">joint to start drawing from</param>
        /// <param name="jointType1">joint to end drawing at</param>
        private void DrawBone(Skeleton skeleton, DrawingContext drawingContext, JointType jointType0, JointType jointType1)
        {
            Joint joint0 = skeleton.Joints[jointType0];
            Joint joint1 = skeleton.Joints[jointType1];

            // If we can't find either of these joints, exit
            if (joint0.TrackingState == JointTrackingState.NotTracked ||
                joint1.TrackingState == JointTrackingState.NotTracked)
            {
                return;
            }

            // Don't draw if both points are inferred
            if (joint0.TrackingState == JointTrackingState.Inferred &&
                joint1.TrackingState == JointTrackingState.Inferred)
            {
                return;
            }

            // We assume all drawn bones are inferred unless BOTH joints are tracked
            Pen drawPen = this.inferredBonePen;
            if (joint0.TrackingState == JointTrackingState.Tracked && joint1.TrackingState == JointTrackingState.Tracked)
            {
                drawPen = this.trackedBonePen;
            }

            drawingContext.DrawLine(drawPen, this.SkeletonPointToScreen(joint0.Position), this.SkeletonPointToScreen(joint1.Position));
        }

        /// <summary>
        /// Handles the checking or unchecking of the seated mode combo box
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void CheckBoxSeatedModeChanged(object sender, RoutedEventArgs e)
        {
            if (null != this.sensor)
            {
                if (this.checkBoxSeatedMode.IsChecked.GetValueOrDefault())
                {
                    this.sensor.SkeletonStream.TrackingMode = SkeletonTrackingMode.Seated;
                }
                else
                {
                    this.sensor.SkeletonStream.TrackingMode = SkeletonTrackingMode.Default;
                }
            }
        }
    }
}