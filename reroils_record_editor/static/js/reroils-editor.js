angular.module('reroilseditor', ['schemaForm'])
    .controller('FormController', function($scope, $http, $window) {
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
                $http({
                        method: 'POST',
                        data: $scope.params.model,
                        url: '/editor/records/save'
                    }).then(function successCallback(response) {
                        $scope.message = response.data.message;
                        $scope.pid = response.data.pid;
                        $window.location.href = '/records/' + response.data.pid;
                    }, function errorCallback(response) {
                        $scope.message.type = 'danger';
                        $scope.message.content = 'An error occurs during the data submission.';
                        $scope.message.title = 'Error: ';
                });
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
