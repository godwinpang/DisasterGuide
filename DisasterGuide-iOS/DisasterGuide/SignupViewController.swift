//
//  SignupViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit
import PromiseKit

class SignupViewController: UIViewController {

    @IBOutlet weak var nameField: UITextField!

    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func onSignUp(_ sender: Any) {
        let username = nameField.text ?? "breaking"
        // TODO will trash if usernameString is empty
        firstly {
            SignupUtils.userSignIn(usernameString: username)
            }.done { _ in
                self.performSegue(withIdentifier: "signUpSegue", sender: nil)
            }.catch { error in
                // Handle Error
        }
    }
    

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        
        //TODO http request to server
    }

}
