$(function() {
  var dt_basic_table = $('.datatables-basic');

  // DataTable with buttons
  // --------------------------------------------------------------------

  if (dt_basic_table.length) {
    dt_basic = dt_basic_table.DataTable({
      ajax: {
            url: 'http://localhost:8000/api/getAllVpn', // لینک API
            // url: 'http://isadid.com/api/getAllVpn', // لینک API
            dataSrc: '' // اگر پاسخ API به صورت لیستی از اشیاء JSON است، این گزینه را خالی بگذارید
        },
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json'
      },
      columns: [
        { data: '' },
        {
          // For Avatar image
          targets: 0,
          orderable: false,
          searchable: false,
          responsivePriority: 1,
          render: function(data, type, full, meta) {
            var id = full['id'];
            var name =full['name']
            var name2 =full['name2']
            if (id) {
              return '<a href="/report/vpn/' + id + '"><img src="' + assetsPath + 'img/vpnIcon/' + name2 + ".png" + '" alt="Avatar" width="60" class="rounded-circle"></a>';
            } else {
              return '';
            }
          }
        },
        {
          // For vpn Name with link
          data: 'name',
          render: function(data, type, full, meta) {
            return '<a href="/report/vpn/' + full['id'] + '">' + data + '</a>';
          }
        }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          orderable: false,
          searchable: false,
          responsivePriority: 2,
          targets: 0,
          render: function(data, type, full, meta) {
            return '';
          }
        }
      ],
      order: [[1, 'asc']],
      dom: '<"card-header flex-column flex-md-row"<"head-label text-center"><"dt-action-buttons text-end pt-3 pt-md-0"B>><"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 d-flex justify-content-center justify-content-md-end"f>>t<"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
      displayLength: 7,
      lengthMenu: [7, 10, 25, 50, 75, 100],
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function(row) {
              var data = row.data();
              return 'جزئیات ' + data['name'];
            }
          }),
          type: 'column',
          renderer: function(api, rowIdx, columns) {

            var data = $.map(columns, function(col, i) {
              console.log('col>>', col);
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                col.rowIndex +
                '" data-dt-column="' +
                col.columnIndex +
                '">' +
                '<td>' +
                col.title +
                ':' +
                '</td> ' +
                '<td>' +
                col.data +
                '</td>' +
                '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      }
    });
    $('div.head-label').html('<h5 class="card-title mb-0">جدول داده با کلید</h5>');
  }
});
