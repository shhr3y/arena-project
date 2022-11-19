//
//  NativeLandmark.swift
//  arena-app
//
//  Created by Shrey Gupta on 16/11/22.
//

import UIKit

// swiftlint:disable identifier_name

class NativeLandmark: Codable {
    let index: Int
    var x: Double
    var y: Double
    var z: Double
    let visibility: Float
    let presence: Float
    var isRemoved: Bool
    
    init(mpLandmark: PoseLandmark) {
        self.index = Int(mpLandmark.index)
        self.x = Double(mpLandmark.x)
        self.y = Double(mpLandmark.y)
        self.z = Double(mpLandmark.z)
        self.visibility = mpLandmark.visibility
        self.presence = mpLandmark.presence
        self.isRemoved = false
    }
    
    func toJson() -> String {
        var dict = [String: Any]()
        dict["index"] = self.index
        dict["x"] = self.x.round(to: 4)
        dict["y"] = self.y.round(to: 4)
        dict["z"] = self.z.round(to: 4)
        dict["visibility"] = self.visibility
        dict["presence"] = self.presence
        dict["isRemoved"] = self.isRemoved
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: dict, options: []) else { return "null"}
        return String(data: jsonData, encoding: String.Encoding.utf8) ?? "null"
    }
}

extension Double {
    /// Rounds the double to decimal places value
    func rounded(toPlaces places:Int) -> Double {
        let divisor = pow(10.0, Double(places))
        return (self * divisor).rounded() / divisor
    }
}
