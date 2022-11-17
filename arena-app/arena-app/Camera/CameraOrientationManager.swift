//
//  CameraOrientationManager.swift
//  arena-app
//
//  Created by Shrey Gupta on 16/11/22.
//

import UIKit
import AVKit

class CameraOrientationManager {
    static let main: CameraOrientationManager = CameraOrientationManager()
    
    var currentOrientation: AVCaptureVideoOrientation?
    
    init() {
        NotificationCenter.default.addObserver(self, selector: #selector(didRotate), name: UIDevice.orientationDidChangeNotification, object: nil)
        updateCurrentOrientationType()
    }
    
    deinit {
        NotificationCenter.default.removeObserver(self, name: UIDevice.orientationDidChangeNotification, object: nil)
    }
    
    // MARK: - Selectors
    @objc private func didRotate() {
        updateCurrentOrientationType()
    }
    
    // MARK: - Helper Functions
    private func updateCurrentOrientationType() {
        let orientation: AVCaptureVideoOrientation = UIApplication.shared.statusBarOrientation == .landscapeLeft ? .landscapeLeft : .landscapeRight
        currentOrientation = orientation
    }
    
    func getOrientationType() -> AVCaptureVideoOrientation {
        return currentOrientation ?? .landscapeLeft
    }
}
