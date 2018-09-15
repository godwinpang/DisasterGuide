//
//  UIUtils.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import Foundation
import UIKit

extension UIButton {
    func addBorder() {
        //button.layer.cornerRadius = 0
        self.layer.borderWidth = 1
        self.layer.borderColor = UIColor.gray.cgColor
    }
}
