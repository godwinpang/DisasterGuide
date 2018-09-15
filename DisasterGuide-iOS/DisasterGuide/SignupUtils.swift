//
//  SignupUtils.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import Foundation
import Parse
import PromiseKit

class SignupUtils {
    static func userSignIn(usernameString: String) -> Promise<String> {
        let newUser = PFUser()
        newUser.username = usernameString
        newUser.password = "test"
        
        return Promise { seal in
            newUser.signUpInBackground { (_: Bool?, error: Error?) in
                if error != nil {
                    seal.reject(error!)
                } else {
                    seal.fulfill("success")
                }
            }
        }
    }
}
