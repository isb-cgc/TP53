/* browse_refs.js */
'use strict';
// const CHECKBOX_COL_ORD = 0;
const REF_ID_COL_ORD = 0;
const AUTHOR_COL_ORD = 1;
const YEAR_COL_ORD = 2;
const TITLE_ID_COL_ORD = 3;
const JOURNAL_COL_ORD = 4;
// const PUBMED_COL_ORD = 5;
const ABSTRACT_COL_ORD = 6;


$(document).ready(function () {

    $('.refs-table thead tr').each(function () {
        $(this).clone(true).appendTo($(this).parents('thead'))
    });


    $('.refs-table').each(function () {
        $($(this).find('thead tr')[1]).find('th').each(function (j) {
            if (j === REF_ID_COL_ORD || j === ABSTRACT_COL_ORD) {
                $(this).html('');
            }
            else {
                var title = $(this).text();
                $(this).html('<input type="text" class="form-control-sm form-control" placeholder="' + title + '" />');
            }

            $('input', this).on('keyup change', function () {
                var table = tables.table($(this).parents('table'));
                if (table.column(j).search() !== this.value) {
                    table
                        .column(j)
                        .search(this.value)
                        .draw();
                }
            });
        });
    });

    var tables = $('.refs-table').DataTable(
        {
            orderCellsTop: true,
            fixedHeader: true,
            order: [[AUTHOR_COL_ORD, "asc"]], //JOURNAL_COL_ORD
            columnDefs: [
                {
                    orderable: false,
                    targets: [REF_ID_COL_ORD, ABSTRACT_COL_ORD]
                },
                {
                    checkboxes: {
                        'selectRow': true
                    },
                    targets: [REF_ID_COL_ORD]
                }
            ],
            select: {
                style: 'multi',
                selector: '.ref-check'
            }
        }
    );



    $('.add-ref').on('click', function () {
        var option_list = '';
        var input_selector = $(this).data('ref-dest');
        var table = tables.table($(this).parents('.modal').find('table'));
        var selected_rows = table.$('tr.selected');
        selected_rows.each(function () {
            var cols = $(this).find('td');
            var ref_id = $(cols[0]).find('input').val();
            option_list += '<option selected value="' + ref_id + '">'
                + $(cols[AUTHOR_COL_ORD]).text()
                + ' (' + $(cols[YEAR_COL_ORD]).text()
                + '). '
                + $(cols[TITLE_ID_COL_ORD]).text()
                + ' <em>'
                + $(cols[JOURNAL_COL_ORD]).text()
                + '</em>'
                + '</option>';
        });
        $(input_selector).find('option').remove();
        $(input_selector).append(option_list);
        $(input_selector).prop('disabled', !option_list.length);
        $(input_selector).trigger("chosen:updated");
    });

    $(".ref-select").on('change', function (evt, params) {
        var ref_id = params['deselected'];
        var selected_checkboxes = $(this).parents('fieldset').siblings('.modal').find('table input:checked[value="'+ref_id+'"]');
        selected_checkboxes.prop("checked", false);
        selected_checkboxes.parents('tr').removeClass('selected');
        $(this).find('option[value="' + ref_id + '"]').remove();
        $(this).prop('disabled', !$(this).find('option').length);
        $(this).trigger('chosen:updated');
    });


});
