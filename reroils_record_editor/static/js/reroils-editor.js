angular.module('reroilseditor', ['schemaForm'])
    .controller('FormController', function($scope, $http, $window) {

        $scope.params = {
            form: ["*"],
            model: {},
            schema: {},
            api_save_url: ''
        };

        $scope.message = {
            title:"",
            content: "",
            type: ""
        };

        function editorInit(init, form, schema, model, api_save_url) {
            $scope.params.schema = angular.fromJson(schema);
            $scope.params.model = angular.fromJson(model);
            $scope.params.form = angular.fromJson(form);
            $scope.params.api_save_url = api_save_url;
        };

        $scope.$on('edit.init', editorInit);
        $scope.importEanFromBnf = function(test) {
          var isbn = $scope.params.model.identifiers.isbn;
          var schema = $scope.params.model['$schema'];
          $http({
              method: 'GET',
                  url: '/editor/import/bnf/ean/' + isbn
              }).then(function successCallback(response) {
                  $scope.params.model = response.data.record;
                  $scope.message.type = response.data.type;
                  $scope.message.content = response.data.content;
                  $scope.message.title = response.data.title;
                  $scope.params.model['$schema'] = schema;
              }, function errorCallback(response) {
                  if (response.status === 404) {
                      $scope.message.type = response.data.type;
                      $scope.message.content = response.data.content;
                      $scope.message.title = response.data.title;
                      $scope.params.model = {'identifiers':{'isbn': isbn}};
                  } else {
                    $scope.message.type = response.data.type;
                      $scope.message.content = response.data.content;
                      $scope.message.title = response.data.title;
                      $scope.params.model = {'identifiers':{'isbn': isbn}};
                  }
                  $scope.params.model['$schema'] = schema;
          });
        }

        $scope.onSubmit = function(form) {
            // First we broadcast an event so all fields validate themselves
            $scope.$broadcast('schemaFormValidate');
            console.log(form.$valid);
            // Then we check if the form is valid
            if (form.$valid) {
                $http({
                        method: 'POST',
                        data: $scope.params.model,
                        url: $scope.params.api_save_url
                    }).then(function successCallback(response) {
                        $window.location.href = response.data.next;
                    }, function errorCallback(response) {
                        $scope.message.type = 'danger';
                        $scope.message.content = response.data.content;
                        $scope.message.title = 'Error:';
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
                    'edit.init', attrs.form, attrs.schema, attrs.model, attrs.apiSaveUrl
                );
            }
        }
    })
    .directive('alert', function() {
        return {
            'template': '<div ng-show="message.title" class="alert alert-{{message.type}}"><strong>{{message.title}}</strong> {{message.content}}</div>'
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
