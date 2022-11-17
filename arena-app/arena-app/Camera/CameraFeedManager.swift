//
//  CameraManager.swift
//  arena-app
//
//  Created by Shrey Gupta on 16/11/22.
//

import UIKit
import AVFoundation

// MARK: - CameraFeedManagerDelegate Declaration
protocol CameraFeedManagerDelegate: AnyObject {
    /**
     This method delivers the pixel buffer of the current frame seen by the device's camera.
     */
    func didOutput(sampleBuffer: CMSampleBuffer)
    
    /**
     This method intimates that the camera permissions have been denied.
     */
    func presentCameraPermissionsDeniedAlert()
    
    /**
     This method intimates that there was an error in video configuration.
     */
    func presentVideoConfigurationErrorAlert()
    
    /**
     This method intimates that a session runtime error occurred.
     */
    func sessionRunTimeErrorOccurred(error: AVError)
    
    /**
     This method intimates that the session was interrupted.
     */
    func sessionWasInterrupted(reason: AVCaptureSession.InterruptionReason, canResumeManually resumeManually: Bool)
    
    /**
     This method intimates that the session interruption has ended.
     */
    func sessionInterruptionEnded()
    
    /**
     This method intimates that during the process an error was encountered.
     */
    func didCaughtError(_ error: Error)
}

/**
 This enum holds the state of the camera initialization.
 */
enum CameraConfiguration {
    case success
    case failed
    case permissionDenied
}

/**
 This class manages all camera related functionality
 */
class CameraFeedManager: NSObject {
    // MARK: - Camera Related Instance Variables
    private let session: AVCaptureSession = AVCaptureSession()
    private let sessionQueue = DispatchQueue(label: "sessionQueue")
    private var cameraConfiguration: CameraConfiguration = .failed
    private lazy var videoDataOutput = AVCaptureVideoDataOutput()
    private var isSessionRunning = false
    
    // MARK: - CameraFeedManagerDelegate
    weak var delegate: CameraFeedManagerDelegate?
    
    
    // MARK: - Initializer based feed type.
    override init() {
        super.init()
        
        // Initializes the session
        session.sessionPreset = .medium
        self.attemptToConfigureSession()
    }
    
    
    // MARK: - Session Start and End methods
    
    /**
     This method starts an AVCaptureSession based on whether the camera/video configuration was successful.
     */
    func checkConfigurationAndStartSession() {
        // don't record session for feedType of video by default.
        
        sessionQueue.async {
            switch self.cameraConfiguration {
            case .success:
                self.addObservers()
                self.startSession()
            case .failed:
                DispatchQueue.main.async {
                    self.delegate?.presentVideoConfigurationErrorAlert()
                }
            case .permissionDenied:
                DispatchQueue.main.async {
                    self.delegate?.presentCameraPermissionsDeniedAlert()
                }
            }
        }
    }
    
    /**
     This method stops a running an AVCaptureSession.
     */
    func stopSession(completion: @escaping(Bool) -> Void) throws {
        self.removeObservers()
        
        sessionQueue.async {
            if self.session.isRunning {
                self.session.stopRunning()
                self.isSessionRunning = self.session.isRunning
            }
        }
    }
    
    func pauseSession(completion: @escaping() -> Void) {
        sessionQueue.async {
            if self.session.isRunning {
                self.session.stopRunning()
                self.isSessionRunning = self.session.isRunning
                DispatchQueue.main.async {
                    completion()
                }
            } else {
                DispatchQueue.main.async {
                    completion()
                }
            }
        }
    }
    
    func resumeSession(completion: @escaping() -> Void) {
        sessionQueue.async {
            self.startSession()
            DispatchQueue.main.async {
                completion()
            }
        }
    }
    
    
    /**
     This method resumes an interrupted AVCaptureSession.
     */
    func resumeInterruptedSession(withCompletion completion: @escaping (Bool) -> Void) {
        sessionQueue.async {
            self.startSession()
            
            DispatchQueue.main.async {
                completion(self.isSessionRunning)
            }
        }
    }
    
    /**
     This method starts the AVCaptureSession
     **/
    private func startSession() {
        self.session.startRunning()
        self.isSessionRunning = self.session.isRunning
    }
    
    // MARK: - Session Configuration Methods.
    /**
     This method requests for camera permissions and handles the configuration of the session and stores the result of configuration or assign delegate for session for video instance to self based on feed type.
     */
    private func attemptToConfigureSession() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            self.cameraConfiguration = .success
        case .notDetermined:
            self.sessionQueue.suspend()
            self.requestCameraAccess(completion: { (_) in
                self.sessionQueue.resume()
            })
        case .denied:
            self.cameraConfiguration = .permissionDenied
        default:
            break
        }
        
        self.sessionQueue.async {
            self.configureCameraSession()
        }
        
    }
    
    /**
     This method requests for camera permissions.
     */
    private func requestCameraAccess(completion: @escaping (Bool) -> Void) {
        AVCaptureDevice.requestAccess(for: .video) { (granted) in
            if !granted {
                self.cameraConfiguration = .permissionDenied
            } else {
                self.cameraConfiguration = .success
            }
            completion(granted)
        }
    }
    
    
    /**
     This method handles all the steps to configure an AVCaptureSession.
     */
    private func configureCameraSession() {
        guard cameraConfiguration == .success else { return }
        session.beginConfiguration()
        
        // Tries to add an AVCaptureDeviceInput.
        guard addVideoDeviceInput() else {
            self.session.commitConfiguration()
            self.cameraConfiguration = .failed
            return
        }
        
        // Tries to add an AVCaptureVideoDataOutput.
        guard addVideoDataOutput() else {
            self.session.commitConfiguration()
            self.cameraConfiguration = .failed
            return
        }
        
        session.commitConfiguration()
        self.cameraConfiguration = .success
    }
    
    /**
     This method tries to add an AVCaptureDeviceInput to the current AVCaptureSession.
     */
    private func addVideoDeviceInput() -> Bool {
        
        /**
         Tries to get the ultrawide back camera. if not available then go with default wide angle camera
         */
        var camera: AVCaptureDevice?
        
        if #available(iOS 13.0, *) {
            if let device = AVCaptureDevice.default(.builtInUltraWideCamera, for: .video, position: .front) {
                camera = device
            } else {
                let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front)
                camera = device
            }
        } else {
            let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front)
            camera = device
        }
        
        guard let camera = camera else {
            let error = NSError(domain: "Cannot find Camera.", code: 001)
            delegate?.didCaughtError(error)
            fatalError("Cannot find camera")
        }
        
        do {
            let videoDeviceInput = try AVCaptureDeviceInput(device: camera)
            if session.canAddInput(videoDeviceInput) {
                session.addInput(videoDeviceInput)
                
                return true
            } else {
                return false
            }
        } catch {
            delegate?.didCaughtError(error)
            fatalError("Cannot create video device input")
        }
    }
    
    /**
     This method sets camera FPS to Int received.
     */
    func changeFPSLimit(limit: Double) {
        do {
            guard let input = session.inputs.first as? AVCaptureDeviceInput else { return }
            
            try input.device.set(frameRate: limit)
        } catch {
            print("DEBUG:- Error occoured while setting FrameRate: \(error.localizedDescription)")
            delegate?.didCaughtError(error)
        }
    }
    
    /**
     This method tries to add an AVCaptureVideoDataOutput to the current AVCaptureSession.
     */
    private func addVideoDataOutput() -> Bool {
        
        let sampleBufferQueue = DispatchQueue(label: "sampleBufferQueue", qos: .userInteractive, attributes: [], autoreleaseFrequency: .workItem)
        videoDataOutput.setSampleBufferDelegate(self, queue: sampleBufferQueue)
        videoDataOutput.alwaysDiscardsLateVideoFrames = true
        videoDataOutput.videoSettings = [ String(kCVPixelBufferPixelFormatTypeKey): kCMPixelFormat_32BGRA]
        
        if session.canAddOutput(videoDataOutput) {
            session.addOutput(videoDataOutput)
            
            DispatchQueue.main.async {
                if #available(iOS 13.0, *) {
                    self.session.connections[0].videoOrientation = CameraOrientationManager.main.getOrientationType()
                    self.session.connections[0].isVideoMirrored = true
                } else {
                    // Fallback on earlier versions
                    self.videoDataOutput.connection(with: .video)?.videoOrientation = CameraOrientationManager.main.getOrientationType()
                    self.videoDataOutput.connection(with: .video)?.isVideoMirrored = true
                }
            }
            
            return true
        }
        
        return false
    }
    
    // MARK: - Notification Observer Handling
    private func addObservers() {
        NotificationCenter.default.addObserver(self, selector: #selector(CameraFeedManager.didStartCaptureSession(notification:)), name: NSNotification.Name.AVCaptureSessionDidStartRunning, object: session)
        NotificationCenter.default.addObserver(self, selector: #selector(CameraFeedManager.didStopCaptureSession(notification:)), name: NSNotification.Name.AVCaptureSessionDidStopRunning, object: session)
        NotificationCenter.default.addObserver(self, selector: #selector(CameraFeedManager.sessionRuntimeErrorOccurred(notification:)), name: NSNotification.Name.AVCaptureSessionRuntimeError, object: session)
        NotificationCenter.default.addObserver(self, selector: #selector(CameraFeedManager.sessionWasInterrupted(notification:)), name: NSNotification.Name.AVCaptureSessionWasInterrupted, object: session)
        NotificationCenter.default.addObserver(self, selector: #selector(CameraFeedManager.sessionInterruptionEnded), name: NSNotification.Name.AVCaptureSessionInterruptionEnded, object: session)
    }
    
    private func removeObservers() {
        NotificationCenter.default.removeObserver(self, name: NSNotification.Name.AVCaptureSessionDidStartRunning, object: session)
        NotificationCenter.default.removeObserver(self, name: NSNotification.Name.AVCaptureSessionDidStopRunning, object: session)
        NotificationCenter.default.removeObserver(self, name: NSNotification.Name.AVCaptureSessionRuntimeError, object: session)
        NotificationCenter.default.removeObserver(self, name: NSNotification.Name.AVCaptureSessionWasInterrupted, object: session)
        NotificationCenter.default.removeObserver(self, name: NSNotification.Name.AVCaptureSessionInterruptionEnded, object: session)
    }
    
    // MARK: - Notification Observers
    @objc func didStartCaptureSession(notification: NSNotification) {
        print("DEBUG:- CAMERA CAPTURE SESSION STARTED")
    }
    
    @objc func didStopCaptureSession(notification: NSNotification) {
        print("DEBUG:- CAMERA CAPTURE SESSION STOPPED")
    }
    
    @objc func sessionWasInterrupted(notification: Notification) {
        
        if let userInfoValue = notification.userInfo?[AVCaptureSessionInterruptionReasonKey] as AnyObject?,
           let reasonIntegerValue = userInfoValue.integerValue,
           let reason = AVCaptureSession.InterruptionReason(rawValue: reasonIntegerValue) {
            print("DEBUG:- Capture session was interrupted with reason \(reason)")
            
            var canResumeManually = false
            if reason == .videoDeviceInUseByAnotherClient {
                canResumeManually = true
            }
            
            self.delegate?.sessionWasInterrupted(reason: reason, canResumeManually: canResumeManually)
        }
    }
    
    @objc func sessionInterruptionEnded(notification: Notification) {
        self.delegate?.sessionInterruptionEnded()
    }
    
    @objc func sessionRuntimeErrorOccurred(notification: Notification) {
        guard let error = notification.userInfo?[AVCaptureSessionErrorKey] as? AVError else { return }
        
        print("DEBUG:- Capture session runtime error: \(error)")
        
        if error.code == .mediaServicesWereReset {
            sessionQueue.async {
                if self.isSessionRunning {
                    self.startSession()
                } else {
                    DispatchQueue.main.async {
                        self.delegate?.sessionRunTimeErrorOccurred(error: error)
                    }
                }
            }
        } else {
            self.delegate?.sessionRunTimeErrorOccurred(error: error)
        }
    }
}

// MARK: - Delegate AVCaptureVideoDataOutputSampleBufferDelegate
extension CameraFeedManager: AVCaptureVideoDataOutputSampleBufferDelegate {
    /**
     This method delegates the CVPixelBuffer of the frame seen by the camera currently.
     */
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        // Passes the sample buffer to the delegators.
        delegate?.didOutput(sampleBuffer: sampleBuffer)
    }
}
