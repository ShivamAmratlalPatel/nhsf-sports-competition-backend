from sqlakeyset import get_page
from sqlalchemy import nulls_first, nulls_last

from backend.schemas import NextPage, PaginationResult, SortBy
from backend.utils import object_to_dict


class GetPaginatedResult:
    def __init__(self) -> None:
        pass

    def run(self, cursor_id, cursor_column, previous, query, schema, per_page=20):
        if cursor_column and cursor_id:
            page = ((cursor_column, cursor_id), previous)
        else:
            page = None

        query_result = get_page(query, per_page=per_page, page=page)
        next = query_result.paging.next
        previous = query_result.paging.previous
        return PaginationResult(
            next=NextPage(
                previous=False,
                cursor_column=next[0][0],
                cursor_id=next[0][1],
            )
            if query_result.paging.has_next
            else None,
            previous=NextPage(
                previous=True,
                cursor_column=previous[0][0],
                cursor_id=previous[0][1],
            )
            if query_result.paging.has_previous
            else None,
            results=[
                object_to_dict(schema.from_orm(ta), format_date=True)
                for ta in query_result
            ],
        )

    def get_sort_by(self, date_column, name_column, sort_by, move_in_column=None):
        if sort_by == SortBy.date_asc:
            return date_column.asc()
        elif sort_by == SortBy.date_desc:
            return date_column.desc()
        elif sort_by == SortBy.a_z_asc:
            return name_column.asc()
        elif sort_by == SortBy.a_z_desc:
            return name_column.desc()
        elif sort_by == SortBy.move_in_asc:
            return nulls_first(move_in_column.asc())
        elif sort_by == SortBy.move_in_desc:
            return nulls_last(move_in_column.desc())
        return None

    def property_attachment_run(
        self,
        cursor_id,
        cursor_column,
        previous,
        query,
        schema,
        per_page=20,
    ):
        if cursor_column and cursor_id:
            page = ((cursor_column, cursor_id), previous)
        else:
            page = None

        query_result = get_page(query, per_page=per_page, page=page)
        next = query_result.paging.next
        previous = query_result.paging.previous
        res = []
        for ta in query_result:
            res.append(
                schema(
                    id=ta[0].id,
                    property_id=ta[0].property_id,
                    kind=ta[0].kind,
                    created_date=ta[0].created_date,
                    file_key=ta[0].file_key,
                    is_verified=ta[0].is_verified,
                    expiry_date=ta[0].expiry_date,
                    description=ta[0].description,
                    display_address=ta[1].display_address,
                ),
            )
        return PaginationResult(
            next=NextPage(
                previous=False,
                cursor_column=next[0][0],
                cursor_id=next[0][1],
            )
            if query_result.paging.has_next
            else None,
            previous=NextPage(
                previous=True,
                cursor_column=previous[0][0],
                cursor_id=previous[0][1],
            )
            if query_result.paging.has_previous
            else None,
            results=res,
        )
