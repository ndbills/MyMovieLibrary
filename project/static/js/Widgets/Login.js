// Set up the namespace
window.mml = window.mml || {};
mml.Widgets = mml.Widgets || {};
  
mml.Widgets.Login = function (options) {
    /// <summary>
    ///     1: Login(options) - This function accepts a JavaScript object containing the options to create a new login widget for a single user.
    /// </summary>
    /// <param name="options" type="object">
    ///     1: url - The url of the service to retrieve data from.&#10;
    ///     2: selector - The jQuery selector for the container the data will be put in.&#10;
    /// </param>
    /// <returns type="mml.Widgets.Login" />
    if (!(this instanceof mml.Widgets.Login)) {
        return new mml.Widgets.Login(options);
    }
    this.init(options); //This will setup the new instance
};
  
mml.Widgets.Login.prototype = (function () {
    var init;
  
    init = function(options){
        var template;
  
        template =  '';
  
        $(options.selectedElement).append(template);
  
    };
  
    /* PUBLIC */
    return {
        init: init
    };
}());