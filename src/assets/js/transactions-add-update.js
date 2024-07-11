'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    let fv; // Declare fv in a scope accessible to both initialization and event listeners

    // Variables for DataTable
    var TransactionDate = $('#transaction-date');
    var DueDate = $('#due-date');
    var select2 = $('.select2');

    if (select2.length) {
      select2.each(function () {
        var $this = $(this);
        $this.wrap('<div class="position-relative"></div>').select2({
          language: "fa",
          placeholder: 'انتخاب وضعیت',
          dropdownParent: $this.parent()
        });

        // Add event listener to clear validation messages on input change
        $this.on('change', function () {
          fv.revalidateField('status');
        });
      });
    }

    // Transaction Date (flatpicker)
    if (TransactionDate) {
      TransactionDate.flatpickr({
        monthSelectorType: 'static',
        locale: 'fa',
        dateFormat: 'Y-m-d',
        onClose: function () {
          fv.revalidateField('due_date');
        }
      });
    }

    // DueDate (flatpicker)
    if (DueDate) {
      DueDate.flatpickr({
        monthSelectorType: 'static',
        dateFormat: 'Y-m-d',
        locale: 'fa',
        onClose: function () {
          fv.revalidateField('due_date');
        }
      });
    }

    const addTransactionForm = document.getElementById('addTransactionForm');
    if (addTransactionForm) {
      // Add New Customer Form Validation
      fv = FormValidation.formValidation(addTransactionForm, {
        fields: {
          customer: {
            validators: {
              notEmpty: {
                message: 'نام مشتری را وارد کنید'
              }
            }
          },
          status: {
            validators: {
              notEmpty: {
                message: 'وضعیت تراکنش را وارد کنید'
              }
            }
          },
          total: {
            validators: {
              notEmpty: {
                message: 'مبلغ را وارد کنید'
              },
              regexp: {
                regexp: /^\d+(\.\d{1,2})?$/,
                message: 'فقط 2 رقم بعد از نقظه مجاز است'
              }
            }
          },
          due_date: {
            validators: {
              notEmpty: {
                message: 'مهلت پرداخت را وارد کنید'
              },
              callback: {
                message: 'مهلت پرداخت باید برابر یا بیشتر از تاریخ ایجاد باشد',
                callback: function (input) {
                  const dueDate = input.value;
                  const transactionDate = TransactionDate.val(); // Use .val() to get the value of jQuery element

                  if (new Date(dueDate) >= new Date(transactionDate)) {
                    return true;
                  }

                  return false;
                }
              }
            }
          },
          transaction_date: {
            validators: {
              notEmpty: {
                message: 'تاریخ شروع را وارد کنید'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-3'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }

    // Update transaction form validation
    const UpdateTransactionForm = document.getElementById('UpdateTransactionForm');
    if (UpdateTransactionForm) {
      fv = FormValidation.formValidation(UpdateTransactionForm, {
        fields: {
          customer: {
            validators: {
              notEmpty: {
                message: 'نام مشتری را وارد کنید'
              }
            }
          },
          status: {
            validators: {
              notEmpty: {
                message: 'وضعیت تراکنش را وارد کنید'
              }
            }
          },
          total: {
            validators: {
              notEmpty: {
                message: 'مبلغ را وارد کنید'
              },
              regexp: {
                regexp: /^\d+(\.\d{1,2})?$/,
                message: 'فقط 2 رقم بعد از نقظه مجاز است'
              }
            }
          },
          due_date: {
            validators: {
              notEmpty: {
                message: 'مهلت پرداخت را وارد کنید'
              },
              callback: {
                message: 'مهلت پرداخت باید برابر یا بیشتر از تاریخ ایجاد باشد',
                callback: function (input) {
                  const dueDate = input.value;
                  const transactionDate = TransactionDate.val(); // Use .val() to get the value of jQuery element

                  if (new Date(dueDate) >= new Date(transactionDate)) {
                    return true;
                  }

                  return false;
                }
              }
            }
          },
          transaction_date: {
            validators: {
              notEmpty: {
                message: 'تاریخ شروع را وارد کنید'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-3'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }
  })();
});
