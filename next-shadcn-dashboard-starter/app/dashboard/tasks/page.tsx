'use client';
import { ColumnDef } from '@tanstack/react-table'; // Assuming you are using tanstack's table for DataTable
import { DataTable } from '@/components/ui/table/data-table';
import { useState, useEffect } from 'react';
import { Heading } from '@/components/ui/heading';
import { Checkbox } from '@/components/ui/checkbox';
import PageContainer from '@/components/layout/page-container';
import { CellAction } from './_components/task-tables/cell-action';
import { Task } from '@/constants/data';
import Link from 'next/link';
import { MessageSquareCode, Plus } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

// Define Task type here

// Define columns for the Task table
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
    accessorKey: 'id', // Key for accessing data
    cell: (info) => info.getValue() // Rendering as a clickable link
  },
  {
    header: 'Type',
    accessorKey: 'workItemType', // Key for accessing data
    cell: (info) => info.getValue() // Display the workItemType value
  },
  {
    header: 'State',
    accessorKey: 'state', // Key for accessing data
    cell: (info) => info.getValue() // Display the state value
  },
  {
    header: 'Title',
    accessorKey: 'title', // Key for accessing data
    cell: (info) => info.getValue() // Display the title value
  },
  {
    id: 'actions',
    cell: ({ row }) => <CellAction data={row.original} /> //
  }
  // {
  //   header: 'URL',
  //   accessorKey: 'url', // Key for accessing data
  //   cell: (info) => info.getValue(), // Display the title value
  // },
];

export default function TaskTable() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stateFilter, setStateFilter] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isAnyFilterActive, setIsAnyFilterActive] = useState<boolean>(false);
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:5000/api/automated_task_assignment/fetch_unassigned_tasks'
        );
        const data = await response.json();

        // Map the response data to match the Task type
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

  // Reset all filters
  const resetFilters = () => {
    setStateFilter(null);
    setSearchQuery('');
    setIsAnyFilterActive(false);
  };

  // Filter the data based on stateFilter and searchQuery
  const filteredData = tasks.filter((task) => {
    const matchesState = stateFilter ? task.state === stateFilter : true;
    const matchesSearchQuery =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.workItemType.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesState && matchesSearchQuery;
  });

  return (
    <PageContainer scrollable>
      <div className="space-y-4 text-black">
        <div className="flex items-start justify-between">
          <Heading
            title="Unassigned WorkItems"
            description="Manage Uassigned Work items"
          />
          <div className='flex'>
            <div className='mx-2'>
              <Link
                href={'/dashboard/tasks'}
                className={cn(buttonVariants({ variant: 'default' }))}
              >
                <MessageSquareCode className="mx-2" />
                Ask AI to Assign
              </Link>
            </div>
            <div className='mx-2'>
              <Link
                href={'/dashboard/tasks'}
                className={cn(buttonVariants({ variant: 'default' }))}
              >
                <Plus className="mx-2" />
                Assign Selected Manually
              </Link>
            </div>
          </div>
        </div>
        <DataTable
          columns={columns}
          data={filteredData}
          totalItems={filteredData.length}
        />
      </div>
    </PageContainer>
  );
}
