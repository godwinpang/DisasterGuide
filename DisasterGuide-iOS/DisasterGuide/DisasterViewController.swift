//
//  DisasterViewController.swift
//  DisasterGuide
//
//  Created by Godwin Pang on 9/15/18.
//  Copyright © 2018 Godwin Pang. All rights reserved.
//

import UIKit
import GoogleMaps

class DisasterViewController: UIViewController {

    @IBOutlet weak var disasterView: UIView!
    
    var mapView: GMSMapView?
    
    override func viewDidLoad() {
        super.viewDidLoad()
 let camera = GMSCameraPosition.camera(withLatitude: -33.86, longitude: 151.20, zoom: 6.0)
        let gmsMapView = GMSMapView.map(withFrame: CGRect(x: 100, y: 200, width: 375, height: 667), camera: camera)
        
        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2D(latitude: -33.86, longitude: 151.20)
        marker.title = "Sydney"
        marker.snippet = "Australia"
        marker.map = gmsMapView
        
        mapView = gmsMapView
        
        mapView?.center = self.view.center
        
        print(view.subviews.count)
        self.view.addSubview(mapView!)
        self.view.bringSubview(toFront: disasterView)
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
