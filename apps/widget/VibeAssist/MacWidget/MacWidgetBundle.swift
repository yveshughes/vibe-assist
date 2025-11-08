//
//  MacWidgetBundle.swift
//  MacWidget
//
//  Created by Yves Hughes on 11/8/25.
//

import WidgetKit
import SwiftUI

@main
struct MacWidgetBundle: WidgetBundle {
    var body: some Widget {
        MacWidget()
        MacWidgetControl()
        // TODO: Add VibeAssistWidget() once VibeAssistWidget.swift is added to MacWidgetExtension target
    }
}
