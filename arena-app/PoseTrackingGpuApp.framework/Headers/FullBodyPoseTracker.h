#import <Foundation/Foundation.h>
#import <CoreVideo/CoreVideo.h>
#import <AVFoundation/AVFoundation.h>

@class PoseLandmark;
@class FullBodyPoseTracker;

@protocol FullBodyPoseTrackerDelegate <NSObject>
- (void)fullBodyPoseTracker: (FullBodyPoseTracker *)tracker didOutputLandmarks: (NSArray<PoseLandmark *> *)landmarks;
- (void)fullBodyPoseTracker: (FullBodyPoseTracker *)tracker didOutputPixelBuffer: (CVPixelBufferRef)pixelBuffer;
@end

@interface FullBodyPoseTracker : NSObject {
    bool isGraphStarted;
}
- (instancetype)init:(int)complexityLevel;
- (void)startGraph;
- (void)changeModelComplexity:(int)complexityLevel;
- (void)sendSampleBuffer:(CVImageBufferRef)pixelBuffer :(CMTime)timestamp;
@property (weak, nonatomic) id <FullBodyPoseTrackerDelegate> delegate;
@property (nonatomic) bool isGraphStarted;
@end

@interface PoseLandmark: NSObject
@property(nonatomic, readonly) int index;
@property(nonatomic) float x;
@property(nonatomic) float y;
@property(nonatomic) float z;
@property(nonatomic, readonly) float visibility;
@property(nonatomic, readonly) float presence;
@end
