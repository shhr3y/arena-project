//
//  SocketService.swift
//  arena-app
//
//  Created by Shrey Gupta on 15/11/22.
//

import Foundation
import SocketIO

protocol SocketServiceDelegate {
    func join()
}
let REF_SERVER = "ws://192.168.0.100:9876/"

class SocketConnection {
    public static let shared = SocketConnection()
    let manager: SocketManager
    
    private init() {
        manager = SocketManager(socketURL: URL(string: REF_SERVER)!, config: [.forceWebsockets(true)])
    }
}

struct SocketService {
    static var shared = SocketService()
    
    var socket: SocketIOClient {
        return SocketConnection.shared.manager.defaultSocket
    }
    
    var delegate: SocketServiceDelegate? {
        didSet {
            setUpListeners()
        }
    }
    
    func setUpListeners() {
//        socket.on("liveUsers") { data, ack in
//            guard let data = data.first as? [String: Any] else { return }
//            let count = data["count"] as? Int ?? 0
//            delegate?.liveUsers(count: count)
//        }
    }
    
    func connectSocket(completion: @escaping () -> Void) {
        if socket.status != .connected{
            socket.connect()
        }
        
        socket.on("connect") {data, ack in
            print("DEBUG:- Socket Connection Established!")
            completion()
            delegate?.join()
        }
        
        socket.on("disconnect") {data, ack in
            print("DEBUG:- Socket Disconnected!")
        }
    }
    
    func disconnectSocket(){
        socket.disconnect()
    }
    
    func sendLandmarks(landmarks: [NativeLandmark]) {
        var jsonLandmarks = [String]()
        for landmark in landmarks {
            jsonLandmarks.append(landmark.toJson())
        }
        socket.emit("landmarks", jsonLandmarks)
    }
}
