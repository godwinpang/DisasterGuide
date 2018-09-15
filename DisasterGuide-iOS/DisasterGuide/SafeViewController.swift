//
//  SafeViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit

class SafeViewController: UIViewController {
    
    @IBOutlet weak var hurricaneButton: UIButton!
    @IBOutlet weak var floodingButton: UIButton!
    @IBOutlet weak var earthquakeButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        hurricaneButton.addBorder()
        floodingButton.addBorder()
        earthquakeButton.addBorder()
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func toEarthquake(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "earthquake") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    @IBAction func toFlooding(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "flooding") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    @IBAction func toHurricane(_ sender: Any) {
        let vc = self.storyboard?.instantiateViewController(
            withIdentifier: "hurricane") as UIViewController!
        navigationController?.pushViewController(vc!, animated: true)
    }
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
