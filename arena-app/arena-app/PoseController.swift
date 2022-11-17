//
//  PoseController.swift
//  arena-app
//
//  Created by Shrey Gupta on 16/11/22.
//

import UIKit

class PoseController: UIViewController {
    //MARK: - Properties
    var camera = CameraFeedManager()
    var tracker = FullBodyPoseTracker(Int32(2))
    
    //MARK: - UI Elements
    private lazy var broadcastView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFit
        imageView.backgroundColor = .random
        return imageView
    }()
    
    //MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        
        camera.delegate = self
        camera.checkConfigurationAndStartSession()
        
        tracker?.delegate = self
        tracker?.startGraph()
        
        
        
        view.addSubview(broadcastView)
        broadcastView.fillSuperview()
        
    }
    //MARK: - Selectors
    
    //MARK: - Helper Functions
    
    
}

extension PoseController: CameraFeedManagerDelegate {
    func didOutput(sampleBuffer: CMSampleBuffer) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        tracker?.sendSampleBuffer(pixelBuffer, CMSampleBufferGetPresentationTimeStamp(sampleBuffer))
    }
    
    func presentCameraPermissionsDeniedAlert() {
        print("presentCameraPermissionsDeniedAlert")
    }
    
    func presentVideoConfigurationErrorAlert() {
        print("presentVideoConfigurationErrorAlert")
    }
    
    func sessionRunTimeErrorOccurred(error: AVError) {
        print("sessionRunTimeErrorOccurred")
    }
    
    func sessionWasInterrupted(reason: AVCaptureSession.InterruptionReason, canResumeManually resumeManually: Bool) {
        print("sessionWasInterrupted")
    }
    
    func sessionInterruptionEnded() {
        print("sessionInterruptionEnded")
    }
    
    func didCaughtError(_ error: Error) {
        print("didCaughtError")
    }
}

extension PoseController: FullBodyPoseTrackerDelegate {
    func fullBodyPoseTracker(_ tracker: FullBodyPoseTracker!, didOutputLandmarks landmarks: [PoseLandmark]!) {
        
    }
    
    func fullBodyPoseTracker(_ tracker: FullBodyPoseTracker!, didOutputPixelBuffer pixelBuffer: CVPixelBuffer!) {
        DispatchQueue.main.async {
            self.broadcastView.image = UIImage(ciImage: CIImage(cvPixelBuffer: pixelBuffer))
        }
    }
}
