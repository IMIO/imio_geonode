console.log("yolo");

if (gxp.plugins.WMSSource) {
    Ext.override(gxp.plugins.WMSSource, {
        createStore: function() {
            var baseParams = this.baseParams || {
                SERVICE: "WMS",
                REQUEST: "GetCapabilities"
            };
            this.version = "1.3.0";
            if (this.version) {
                baseParams.VERSION = this.version;
            }
            this.format = new OpenLayers.Format.WMSCapabilities({keepData: true,defaultVersion: "1.3.0"});
            var lazy = this.isLazy();

            this.store = new GeoExt.data.WMSCapabilitiesStore({
                // Since we want our parameters (e.g. VERSION) to override any in the
                // given URL, we need to remove corresponding paramters from the
                // provided URL.  Simply setting baseParams on the store is also not
                // enough because Ext just tacks these parameters on to the URL - so
                // we get requests like ?Request=GetCapabilities&REQUEST=GetCapabilities
                // (assuming the user provides a URL with a Request parameter in it).
                url: this.trimUrl(this.url, baseParams),
                baseParams: baseParams,
                format: this.format,
                autoLoad: !lazy,
                layerParams: {exceptions: null},
                listeners: {
                    load: function() {
                        // The load event is fired even if a bogus capabilities doc
                        // is read (http://trac.geoext.org/ticket/295).
                        // Until this changes, we duck type a bad capabilities
                        // object and fire failure if found.
                        if (!this.store.reader.raw || !this.store.reader.raw.service) {
                            this.fireEvent("failure", this, "Invalid capabilities document.");
                        } else {
                            if (!this.title) {
                                this.title = this.store.reader.raw.service.title;
                            }
                            if (!this.ready) {
                                this.ready = true;
                                this.fireEvent("ready", this);
                            } else {
                                this.lazy = false;
                                //TODO Here we could update all records from this
                                // source on the map that were added when the
                                // source was lazy.
                            }
                        }
                        // clean up data stored on format after parsing is complete
                        delete this.format.data;
                    },
                    exception: function(proxy, type, action, options, response, error) {
                        delete this.store;
                        var msg, details = "";
                        if (type === "response") {
                            if (typeof error == "string") {
                                msg = error;
                            } else {
                                msg = "Invalid response from server.";
                                // special error handling in IE
                                var data = this.format && this.format.data;
                                if (data && data.parseError) {
                                    msg += "  " + data.parseError.reason + " - line: " + data.parseError.line;
                                }
                                var status = response.status;
                                if (status >= 200 && status < 300) {
                                    // TODO: consider pushing this into GeoExt
                                    var report = error && error.arg && error.arg.exceptionReport;
                                    details = gxp.util.getOGCExceptionText(report);
                                } else {
                                    details = "Status: " + status;
                                }
                            }
                        } else {
                            msg = "Trouble creating layer store from response.";
                            details = "Unable to handle response.";
                        }
                        // TODO: decide on signature for failure listeners
                        this.fireEvent("failure", this, msg, details);
                        // clean up data stored on format after parsing is complete
                        delete this.format.data;
                    },
                    scope: this
                }
            });
            if (lazy) {
                this.lazy = lazy;
                this.ready = true;
                this.fireEvent("ready", this);
            }
        }
    });
}
