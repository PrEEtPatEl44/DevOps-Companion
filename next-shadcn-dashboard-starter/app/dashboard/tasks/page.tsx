"use client"
import { useState, useEffect } from 'react';
import { ColumnDef, useReactTable, getCoreRowModel, getPaginationRowModel } from '@tanstack/react-table';
import { DataTable } from '@/components/ui/table/data-table';
import { Heading } from '@/components/ui/heading';
import { Checkbox } from '@/components/ui/checkbox';
import PageContainer from '@/components/layout/page-container';
import { CellAction } from './_components/task-tables/cell-action';
import { Task } from '@/constants/data';
import Link from 'next/link';
import { MessageSquareCode } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

const columns: ColumnDef<Task, unknown>[] = [
  {
    id: 'select',
    header: ({ table }) => (
      <Checkbox
        checked={table.getIsAllPageRowsSelected()}
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false
  },
  {
    header: 'ID',
    accessorKey: 'id',
    cell: (info) => info.getValue()
  },
  {
    header: 'Type',
    accessorKey: 'workItemType',
    cell: (info) => info.getValue()
  },
  {
    header: 'State',
    accessorKey: 'state',
    cell: (info) => info.getValue()
  },
  {
    header: 'Title',
    accessorKey: 'title',
    cell: (info) => info.getValue()
  },
  {
    id: 'actions',
    cell: ({ row }) => <CellAction data={row.original} />
  }
];

export default function TaskTable() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [rowSelection, setRowSelection] = useState({});

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:5000/api/automated_task_assignment/fetch_unassigned_tasks'
        );
        const data = await response.json();

        const fetchedTasks = data.workItems.map((item: any) => ({
          id: item.id,
          url: item.url,
          workItemType: item.fields['System.WorkItemType'],
          state: item.fields['System.State'],
          title: item.fields['System.Title']
        }));

        setTasks(fetchedTasks);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, []);

  const table = useReactTable({
    data: tasks,
    columns,
    state: { rowSelection },
    getCoreRowModel: getCoreRowModel(),
    onRowSelectionChange: setRowSelection,
    getPaginationRowModel: getPaginationRowModel(),
  });

  const selectedRows = table
    .getSelectedRowModel()
    .rows.map((row) => row.original);

  return (
    <PageContainer scrollable>
      <div className="space-y-4 text-black">
        <div className="flex items-start justify-between">
          <Heading
            title="Unassigned WorkItems"
            description="Manage Unassigned Work items"
          />
          <div className='flex'>
            <div className='mx-2'>
              <button
                onClick={() => console.log(selectedRows)}
                className={cn(buttonVariants({ variant: 'default' }))}
              >
                <MessageSquareCode className="mx-2" />
                Ask AI to Assign
              </button>
            </div>
          </div>
        </div>
        <DataTable
  columns={columns}
  data={tasks}
  totalItems={tasks.length}
/>
      </div>
    </PageContainer>
  );
}
