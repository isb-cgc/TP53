/* browse_refs.js */
'use strict';
const REF_ID_COL_ORD = 0;
const AUTHOR_COL_ORD = 1;
const YEAR_COL_ORD = 2;
const TITLE_ID_COL_ORD = 3;
const JOURNAL_COL_ORD = 4;
// const PUBMED_COL_ORD = 5;
const ABSTRACT_COL_ORD = 6;


$(document).ready(function () {
    var ref_tables = $('.refs-table');
    $('.refs-table thead tr').each(function () {
        $(this).clone(true).appendTo($(this).parents('thead'))
    });

    ref_tables.each(function () {
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

    var tables = ref_tables.DataTable(
        {
            orderCellsTop: true,
            fixedHeader: true,
            order: [[AUTHOR_COL_ORD, "asc"]], //JOURNAL_COL_ORD
            page: 'current',
            columnDefs: [
                {
                    orderable: false,
                    targets: [REF_ID_COL_ORD, ABSTRACT_COL_ORD]
                }
            ],
            select: {
                style: 'multi',
                selector: '.ref-check'
            },
            lengthMenu: [5,10,25]

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

    $('.reset-ref').on('click', function () {
        // reset row selections
        var selected_table = $(this).parents('.modal').find('table');
        var table = tables.table(selected_table);
        table.rows().deselect(); // deselect datatables row selection
        selected_table.find('input:checkbox').prop('checked', false); // deselect all checkboxes
        selected_table.find('input:text').val('').change();
    });

    // events

    $(".ref-select").on('change', function (evt, params) {
        // if reference selection has been deleted from the chosen.js UI update the modal's checkboxes
        if (params){
            var deselected_ref_id = params['deselected'];
            var selected_checkboxes = $(this).parents('fieldset').siblings('.modal').find('table input:checked[value="'+deselected_ref_id+'"]');
            selected_checkboxes.prop("checked", false);

            $(this).find('option[value="' + deselected_ref_id + '"]').remove();
            $(this).prop('disabled', !$(this).find('option').length);
            $(this).trigger('chosen:updated');
        }
        else{
            // if event is triggered by clicking on 'clear-all'
            $('.reset-ref').trigger('click');
        }
    });

    $('input.ref-check-all').on('change', function (e) {
        // checkbox to select all (filtered rows) is changed update the row selection
        var is_checked = $(this).is(':checked');
        var table = tables.table($(this).parents('table'));
        selectFilteredRows(table, is_checked);
    });

});


var selectFilteredRows = function (t, bool) {
    var selection = '';
    if (bool) {
        t.rows({search: 'applied'}).select();
        selection = 'tr.selected';
    }
    else {
        t.rows().deselect();
        selection = 'tr'
    }
    t.$(selection).find('input.ref-check').prop('checked', bool);
};

