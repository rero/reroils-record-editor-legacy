angular.module('reroilseditor', ['schemaForm'])
    .controller('FormController', function($scope) {
        $scope.params = {
            form: ["*"],
            model: {},
            schema: {}
        };
        $scope.message = {
            title:"",
            content: "",
            type: ""
        };
        function editorInit(init, form, schema, model) {
            $scope.params.schema = angular.fromJson(schema);
            $scope.params.model = angular.fromJson(model);
            $scope.params.form = angular.fromJson(form);
        };
        $scope.$on('edit.init', editorInit);
        $scope.onSubmit = function(form) {
            // First we broadcast an event so all fields validate themselves
            $scope.$broadcast('schemaFormValidate');

            // Then we check if the form is valid
            if (form.$valid) {
                console.log('Valid');
            }
        }
    })
    .directive('ngInitial', function($parse) {
        return {
            restrict: 'E',
            scope: false,
            controller: 'FormController',
            link: function (scope, element, attrs) {
                scope.$broadcast(
                    'edit.init', attrs.form, attrs.schema, attrs.model
                );
            }
        }
    });

(function (angular) {
    // Bootstrap it!
    angular.element(document).ready(function() {
        angular.bootstrap(
            document.getElementById("reroils-editor"), [
                'schemaForm',
                'reroilseditor'
            ]
        );
    });
})(angular);
