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
    var x: Float
    var y: Float
    var z: Float
    let visibility: Float
    let presence: Float
    var isRemoved: Bool
    
    init(mpLandmark: PoseLandmark) {
        self.index = Int(mpLandmark.index)
        self.x = mpLandmark.x
        self.y = mpLandmark.y
        self.z = mpLandmark.z
        self.visibility = mpLandmark.visibility
        self.presence = mpLandmark.presence
        self.isRemoved = false
    }
    
    func toJson() -> String {
        var dict = [String: Any]()
        dict["index"] = self.index
        dict["x"] = self.x
        dict["y"] = self.y
        dict["z"] = self.z
        dict["visibility"] = self.visibility
        dict["presence"] = self.presence
        dict["isRemoved"] = self.isRemoved
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: dict, options: []) else { return "nUll"}
        print(jsonData)
        return String(data: jsonData, encoding: String.Encoding.utf8) ?? "null"
    }
}
