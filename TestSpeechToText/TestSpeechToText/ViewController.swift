//
//  ViewController.swift
//  TestSpeechToText
//
//  Created by Geeling Chau on 9/15/18.
//  Copyright © 2018 Geeling Chau. All rights reserved.
//

import UIKit
import Speech

class ViewController: UIViewController {

    @IBOutlet weak var textLabel: UILabel!
    
    var isListening = false
    let audioEngine = AVAudioEngine()
    let speechRecognizer: SFSpeechRecognizer? = SFSpeechRecognizer()
    
    let request = SFSpeechAudioBufferRecognitionRequest()
    var recognitionTask: SFSpeechRecognitionTask?
    


    func requestTranscribePermissions() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                if authStatus == .authorized {
                    print("Good to go!")
                } else {
                    print("Transcription permission was declined.")
                }
            }
        }
    }

    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.requestTranscribePermissions()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func toggleS2T(_ sender: Any) {
        if(isListening) {
            isListening = false
        } else {
            isListening = true
            self.recordAndRecognizeSpeech()
            
        }
        textLabel.text = "mwahahahahaha"
    }
    
    func recordAndRecognizeSpeech() {
        let node = audioEngine.inputNode
        let recordingFormat = node.outputFormat(forBus:0)
        node.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in self.request.append(buffer)
        }
        
        audioEngine.prepare()
        do {
            try audioEngine.start()
        } catch {
            return print(error)
        }
        
        guard let myRecognizer = SFSpeechRecognizer() else { return }
        
        if !myRecognizer.isAvailable {
            return
        }
        
        recognitionTask = speechRecognizer?.recognitionTask(with: request, resultHandler: { result, error in
            if let result = result {
                let bestString = result.bestTranscription.formattedString
                self.textLabel.text = bestString
                
            } else if let error = error {
                print(error)
                
            }})
        
    }
    
}

