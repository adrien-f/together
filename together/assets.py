
import os
from flask.ext.assets import Bundle, Environment
from webassets.filter.jst import JSTemplateFilter

assets_env = Environment()

common_css = Bundle(
    '../static/less/*.less',
    filters='less',
    output='../public/css/common.css'
)
assets_env.register('common_css', common_css)

common_js = Bundle(
    '../static/bower_components/jquery/dist/jquery.js',
    '../static/bower_components/bootstrap/dist/js/bootstrap.js',
    '../static/bower_components/moment/moment.js',
    Bundle(
        '../static/bower_components/angular/angular.js',
        '../static/bower_components/angular-route/angular-route.js',
        '../static/bower_components/angular-resource/angular-resource.js',
        '../static/bower_components/angular-moment/angular-moment.js',
        '../static/bower_components/angular-bootstrap/ui-bootstrap.js',
        '../static/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
    ),
    output='../public/js/common.js'
)
assets_env.register('common_js', common_js)

application_js = Bundle(
    '../static/coffee/*.coffee',
    filters='coffeescript',
    output='../public/js/application.js'
)
assets_env.register('application_js', application_js)


class AngularJST(JSTemplateFilter):
    def setup(self):
        super(AngularJST, self).setup()

    def process_templates(self, out, hunks, **kwargs):
        out.write("angular.module('TogetherApp').run(['$templateCache', function($templateCache) {")
        for name, hunk in self.iter_templates_with_base(hunks):
            # Make it a valid Javascript string. Is this smart enough?
            contents = hunk.data().replace('\n', '\\n').replace("'", r"\'")
            out.write("$templateCache.put('%s', " % (os.path.basename(hunk.filename).replace('__', '/')))
            out.write("'%s');" % (contents))
        out.write("}]);")

angular_jst = AngularJST()

application_templates = Bundle(
    '../templates/angular/*.html',
    filters=angular_jst,
    output='../public/js/application-templates.js'
)
assets_env.register('application_templates', application_templates)
