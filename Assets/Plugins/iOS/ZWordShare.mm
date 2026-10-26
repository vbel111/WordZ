// Word Z - opens the iOS share sheet (UIActivityViewController). Called from Share.cs via DllImport("__Internal").
#import <UIKit/UIKit.h>

extern UIViewController* UnityGetGLViewController();

extern "C" void _ZWordShareText(const char* text, const char* url)
{
    NSString* body = [NSString stringWithUTF8String:(text ? text : "")];
    NSMutableArray* items = [NSMutableArray arrayWithObject:body];
    if (url != NULL && strlen(url) > 0)
    {
        NSURL* link = [NSURL URLWithString:[NSString stringWithUTF8String:url]];
        if (link != nil) [items addObject:link];
    }

    dispatch_async(dispatch_get_main_queue(), ^{
        UIViewController* root = UnityGetGLViewController();
        UIActivityViewController* sheet = [[UIActivityViewController alloc] initWithActivityItems:items applicationActivities:nil];
        // iPad needs an anchor for the popover
        UIPopoverPresentationController* pop = sheet.popoverPresentationController;
        if (pop != nil)
        {
            pop.sourceView = root.view;
            pop.sourceRect = CGRectMake(root.view.bounds.size.width / 2, root.view.bounds.size.height / 2, 1, 1);
            pop.permittedArrowDirections = 0;
        }
        [root presentViewController:sheet animated:YES completion:nil];
    });
}
