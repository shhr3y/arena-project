//
//  ViewController.swift
//  arena-app
//
//  Created by Shrey Gupta on 15/11/22.
//

import UIKit

class ViewController: UIViewController {
    
    private lazy var connectButton: UIButton = {
        let button = UIButton(type: .system)
        button.setTitle("Connect", for: .normal)
        button.addTarget(self, action: #selector(didTapConnect), for: .touchUpInside)
        return button
    } ()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        view.backgroundColor = .white
        
        view.addSubview(connectButton)
        connectButton.centerX(inView: self.view)
        connectButton.centerY(inView: self.view)
    }
    
    @objc func didTapConnect() {
        SocketService.shared.connectSocket {
            self.navigationController?.pushViewController(PoseController(), animated: true)
        }
    }


}

