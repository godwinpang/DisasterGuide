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
        self.layer.borderWidth = 1
        self.layer.borderColor = UIColor.dGray.cgColor
    }
}

extension UIColor {
    
    static func hexStringToUIColor (hex: String) -> UIColor {
        var cString:String = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
        
        if (cString.hasPrefix("#")) {
            cString.remove(at: cString.startIndex)
        }
        
        if ((cString.count) != 6) {
            return UIColor.gray
        }
        
        var rgbValue:UInt32 = 0
        Scanner(string: cString).scanHexInt32(&rgbValue)
        
        return UIColor(
            red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
            green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
            blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
            alpha: CGFloat(1.0)
        )
    }
    
    static let dRed = UIColor.hexStringToUIColor(hex: "C66E64")
    static let dBlue = UIColor.hexStringToUIColor(hex: "4B70CC")
    static let dBlack = UIColor.hexStringToUIColor(hex: "51534F")
    static let dGreen = UIColor.hexStringToUIColor(hex: "90AB89")
    static let dOrange = UIColor.hexStringToUIColor(hex: "EAB28C")
    //static let dGray = UIColor.hexStringToUIColor(hex: "767774")
    static let dGray = UIColor(red: CGFloat(118 / 255.0), green: CGFloat(119 / 255.0), blue: CGFloat(116 / 255.0), alpha: CGFloat(1.0))
    
}
